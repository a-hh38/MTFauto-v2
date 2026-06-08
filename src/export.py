import os
from datetime import datetime

import pandas as pd

from frequency import (
    get_daily_data,
    get_monthly_data
)


def export_history(
    history_file,
    trend_file,
    frequency,
    use_default=False
):

    frequency = frequency.lower()

    os.makedirs(
        "output",
        exist_ok=True
    )

    stock_df = pd.read_csv(
        history_file
    )

    trend_df = pd.read_csv(
        trend_file
    )

    stock_df["Date"] = pd.to_datetime(
        stock_df["Date"]
    )

    trend_df["Date"] = pd.to_datetime(
        trend_df["Date"]
    )

    print(
        f"\nFrequency Selected: {frequency}"
    )

    # -------------------------
    # Daily
    # -------------------------

    if frequency == "daily":

        final_df = get_daily_data(
            stock_df
        )

        sheet_name = "Daily_Data"

        if use_default:

            daily_dates = (
                final_df["Date"]
                .drop_duplicates()
                .sort_values()
            )

            print(
                f"Unique Trading Dates Available: {len(daily_dates)}"
            )

            last_90_dates = daily_dates.tail(90)

            print(
                f"Trading Dates Selected: {len(last_90_dates)}"
            )

            print(
                f"First Trading Date: {last_90_dates.min()}"
            )

            print(
                f"Last Trading Date: {last_90_dates.max()}"
            )

            final_df = final_df[
                final_df["Date"].isin(
                    last_90_dates
                )
            ]

            trend_export = trend_df[
                trend_df["Date"].isin(
                    last_90_dates
                )
            ]

        else:

            trend_export = trend_df

    # -------------------------
    # Monthly
    # -------------------------

    elif frequency == "monthly":

        final_df = get_monthly_data(
            stock_df
        )

        sheet_name = "Monthly_Data"

        month_end_dates = (
            trend_df.groupby(
                [
                    trend_df["Date"].dt.year,
                    trend_df["Date"].dt.month
                ]
            )["Date"]
            .max()
            .tolist()
        )

        trend_export = trend_df[
            trend_df["Date"].isin(
                month_end_dates
            )
        ]

    else:

        raise ValueError(
            f"Unknown frequency: {frequency}"
        )

    # -------------------------
    # Output File Name
    # -------------------------

    start_date = (
        final_df["Date"]
        .min()
        .strftime("%d%b%Y")
    )

    end_date = (
        final_df["Date"]
        .max()
        .strftime("%d%b%Y")
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    output_file = (
        f"mrg_trading_"
        f"{frequency}_"
        f"{start_date}_to_"
        f"{end_date}_"
        f"{timestamp}.xlsx"
    )

    # -------------------------
    # Trend Analytics
    # -------------------------

    trend_export = trend_export.sort_values(
        "Date"
    )

    trend_export["GrowthPct"] = (
        trend_export["ClosingOutstanding"]
        .pct_change()
        * 100
    )

    # -------------------------
    # Excel Export
    # -------------------------

    with pd.ExcelWriter(
        output_file,
        engine="openpyxl"
    ) as writer:

        final_df.to_excel(
            writer,
            sheet_name=sheet_name,
            index=False
        )

        trend_export.to_excel(
            writer,
            sheet_name="MTF_Trend",
            index=False
        )

        trend_export[
            [
                "Date",
                "NetGrowth",
                "GrowthPct",
                "ClosingOutstanding"
            ]
        ].to_excel(
            writer,
            sheet_name="Trend_Analytics",
            index=False
        )

    print(
        f"\nExported: {output_file}"
    )

    return output_file
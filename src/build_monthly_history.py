from datetime import timedelta
import pandas as pd

from download_mtf import download_report
from parse_mtf import parse_report


def get_last_trading_day(year, month):

    if month == 12:

        current = pd.Timestamp(
            year + 1,
            1,
            1
        ) - timedelta(days=1)

    else:

        current = pd.Timestamp(
            year,
            month + 1,
            1
        ) - timedelta(days=1)

    while True:

        try:

            zip_file = download_report(
                current
            )

            if zip_file:

                return current

        except:

            pass

        current -= timedelta(days=1)


def build_monthly_history(
    start_date,
    end_date
):

    all_stock_data = []
    all_summary_data = []

    months = pd.period_range(
        start=start_date,
        end=end_date,
        freq="M"
    )

    for month in months:

        trading_day = get_last_trading_day(
            month.year,
            month.month
        )

        print(
            f"Processing Month End: "
            f"{trading_day.strftime('%d-%m-%Y')}"
        )

        try:

            zip_file = download_report(
                trading_day
            )

            summary_df, stock_df = parse_report(
                zip_file,
                trading_day.date()
            )

            all_stock_data.append(
                stock_df
            )

            all_summary_data.append(
                summary_df
            )

            print(
                f"Stock Rows: {len(stock_df)}"
            )

        except Exception as e:

            print(
                f"Error: {e}"
            )

    stock_history = pd.concat(
        all_stock_data,
        ignore_index=True
    )

    summary_history = pd.concat(
        all_summary_data,
        ignore_index=True
    )

    history_file = (
        "data/processed/"
        "mtf_history_monthly.csv"
    )

    trend_file = (
        "data/processed/"
        "mtf_trend_monthly.csv"
    )

    stock_history.to_csv(
        history_file,
        index=False
    )

    summary_history.to_csv(
        trend_file,
        index=False
    )

    print(
        f"\nSaved: {history_file}"
    )

    print(
        f"Saved: {trend_file}"
    )

    return (
        history_file,
        trend_file
    )
from datetime import timedelta
import pandas as pd
from pathlib import Path
from download_mtf import download_report
from parse_mtf import parse_report


def build_history(start_date, end_date):

    all_stock_data = []
    all_summary_data = []

    current = start_date

    while current <= end_date:

        print(
            f"Processing {current.strftime('%d-%m-%Y')}"
        )

        try:

            zip_file = download_report(current)

            if zip_file:

                summary_df, stock_df = parse_report(
                    zip_file,
                    current.date()
                )

                all_summary_data.append(summary_df)
                all_stock_data.append(stock_df)

                print(
                    f"Stock Rows: {len(stock_df)}"
                )

        except Exception as e:

            print(
                f"Error: {e}"
            )

        current += timedelta(days=1)

    stock_history = pd.concat(
        all_stock_data,
        ignore_index=True
    )

    summary_history = pd.concat(
        all_summary_data,
        ignore_index=True
    )


    Path("data/processed").mkdir(
        parents=True,
        exist_ok=True
    )

    start_str = start_date.strftime("%d%m%Y")
    end_str = end_date.strftime("%d%m%Y")

    history_file = (
        f"data/processed/"
        f"mtf_history_{start_str}_{end_str}.csv"
    )

    trend_file = (
        f"data/processed/"
        f"mtf_trend_{start_str}_{end_str}.csv"
    )

    stock_history.to_csv(
        history_file,
        index=False
    )

    summary_history.to_csv(
        trend_file,
        index=False
    )

    print(f"\nSaved: {history_file}")
    print(f"Saved: {trend_file}")

    return history_file, trend_file
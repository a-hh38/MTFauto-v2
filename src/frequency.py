import pandas as pd


def get_daily_data(df):

    df = df.copy()

    df["Date"] = pd.to_datetime(
        df["Date"]
    )

    return (
        df.sort_values(
            ["Date", "Symbol"]
        )
        .reset_index(drop=True)
    )


def get_monthly_data(df):

    df = df.copy()

    df["Date"] = pd.to_datetime(
        df["Date"]
    )

    month_end_dates = (
        df.groupby(
            [
                df["Date"].dt.year,
                df["Date"].dt.month
            ]
        )["Date"]
        .max()
        .tolist()
    )

    monthly_df = df[
        df["Date"].isin(
            month_end_dates
        )
    ]

    return (
        monthly_df
        .sort_values(
            ["Date", "Symbol"]
        )
        .reset_index(drop=True)
    )
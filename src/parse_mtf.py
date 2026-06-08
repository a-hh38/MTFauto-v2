import pandas as pd
import zipfile


def parse_report(zip_path, report_date):

    with zipfile.ZipFile(zip_path, "r") as z:

        csv_file = z.namelist()[0]

        raw = pd.read_csv(
            z.open(csv_file),
            header=None
        )

        # -------------------------
        # Summary Section
        # -------------------------

        opening = float(raw.iloc[4, 2])
        fresh = float(raw.iloc[5, 2])
        liquidated = float(raw.iloc[6, 2])
        closing = float(raw.iloc[7, 2])

        summary_df = pd.DataFrame({
            "Date": [report_date],
            "OpeningOutstanding": [opening],
            "FreshExposure": [fresh],
            "ExposureLiquidated": [liquidated],
            "ClosingOutstanding": [closing]
        })

        summary_df["NetGrowth"] = (
            summary_df["FreshExposure"]
            - summary_df["ExposureLiquidated"]
        )

        # -------------------------
        # Stock Section
        # -------------------------

        header_idx = raw[
            raw.iloc[:, 0] == "Symbol"
        ].index[0]

        stock_df = pd.read_csv(
            z.open(csv_file),
            header=header_idx
        )

        stock_df.columns = [
            "Symbol",
            "Name",
            "QtyFinanced",
            "AmtFinanced"
        ]

        stock_df["Date"] = report_date

        # Remove blank rows
        stock_df = stock_df.dropna(
            subset=["Symbol"]
        )

        # Convert numeric columns
        stock_df["QtyFinanced"] = pd.to_numeric(
            stock_df["QtyFinanced"],
            errors="coerce"
        )

        stock_df["AmtFinanced"] = pd.to_numeric(
            stock_df["AmtFinanced"],
            errors="coerce"
        )

        # Remove footer rows like:
        # "* Figures are rounded to the nearest decimal."
        stock_df = stock_df[
            stock_df["QtyFinanced"].notna()
        ]

        stock_df = stock_df.reset_index(
            drop=True
        )

        return summary_df, stock_df
import streamlit as st
from datetime import datetime, date, timedelta
import sys
import shutil
from pathlib import Path

sys.path.append("src")

from build_history import build_history
from build_monthly_history import build_monthly_history
from export import export_history

st.sidebar.success(
    "MTF V2 CLEAN DEPLOY"
)

st.set_page_config(
    page_title="MTF History Builder",
    layout="centered"
)

st.title("MTF History Builder")

st.markdown(
    "Generate MTF reports from NSE Margin Trading Disclosure data."
)

today = date.today()

# NSE data generally lags by a couple of trading days
latest_available_date = (
    today - timedelta(days=4)
)

default_start = (
    latest_available_date
    - timedelta(days=90)
).strftime("%d-%m-%Y")

default_end = (
    latest_available_date
).strftime("%d-%m-%Y")

frequency = st.selectbox(
    "Frequency",
    [
        "Daily",
        "Monthly"
    ]
)

# -------------------------
# Daily
# -------------------------

if frequency == "Daily":

    use_default = st.checkbox(
        "Use Default Last 90 Days",
        value=True
    )

    if use_default:

        start_date_str = st.text_input(
            "Start Date (DD-MM-YYYY)",
            value=default_start
        )

        end_date_str = st.text_input(
            "End Date (DD-MM-YYYY)",
            value=default_end
        )

    else:

        start_date_str = st.text_input(
            "Start Date (DD-MM-YYYY)"
        )

        end_date_str = st.text_input(
            "End Date (DD-MM-YYYY)"
        )

# -------------------------
# Monthly
# -------------------------

else:

    use_default = False

    start_date_str = st.text_input(
        "Start Date (DD-MM-YYYY)"
    )

    end_date_str = st.text_input(
        "End Date (DD-MM-YYYY)"
    )

# -------------------------
# Generate
# -------------------------

if st.button(
    "Generate Report",
    use_container_width=True
):

    try:

        start_date = datetime.strptime(
            start_date_str,
            "%d-%m-%Y"
        )

        end_date = datetime.strptime(
            end_date_str,
            "%d-%m-%Y"
        )

    except ValueError:

        st.error(
            "Invalid date format. Use DD-MM-YYYY."
        )

        st.stop()

    if start_date > end_date:

        st.error(
            "Start date cannot be after end date."
        )

        st.stop()

    # -------------------------
    # Clear old files
    # -------------------------

    for folder in [
        "data/raw",
        "data/processed",
        "output"
    ]:

        path = Path(folder)

        if path.exists():

            shutil.rmtree(path)

        path.mkdir(
            parents=True,
            exist_ok=True
        )

    with st.spinner(
        "Building report..."
    ):

        if frequency == "Daily":

            history_file, trend_file = (
                build_history(
                    start_date,
                    end_date
                )
            )

        else:

            history_file, trend_file = (
                build_monthly_history(
                    start_date,
                    end_date
                )
            )

        output_file = export_history(
            history_file,
            trend_file,
            frequency,
            use_default
        )

    st.success(
        "Report generated successfully!"
    )

    with open(
        output_file,
        "rb"
    ) as file:

        st.download_button(
            label="Download Excel Report",
            data=file,
            file_name=output_file.split("/")[-1],
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
from pathlib import Path
import requests

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)


def download_report(report_date):

    filename = f"mrg_trading_{report_date.strftime('%d%m%y')}.zip"

    url = (
        f"https://nsearchives.nseindia.com/content/equities/{filename}"
    )

    file_path = RAW_DIR / filename

    if file_path.exists():
        return file_path

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/137.0 Safari/537.36"
        )
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=60
    )

    if response.status_code == 200:
        file_path.write_bytes(response.content)
        return file_path

    return None
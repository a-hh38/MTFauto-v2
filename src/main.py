from datetime import datetime

from build_history import build_history
from export import export_history

print("\n=== MTF History Builder ===\n")

start_date_str = input(
    "Enter Start Date (DD-MM-YYYY): "
)

end_date_str = input(
    "Enter End Date (DD-MM-YYYY): "
)

print("\nSelect Frequency:")
print("1. Daily")
print("2. Monthly")

frequency_choice = input(
    "\nEnter choice (1/2): "
)

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

    print(
        "\nInvalid date format. Use DD-MM-YYYY"
    )

    exit()

if start_date > end_date:

    print(
        "\nStart Date cannot be after End Date."
    )

    exit()

if frequency_choice == "1":
    frequency = "daily"

elif frequency_choice == "2":
    frequency = "monthly"

else:

    print(
        "\nInvalid choice."
    )

    exit()

print(
    f"\nBuilding history from "
    f"{start_date.date()} "
    f"to "
    f"{end_date.date()}\n"
)

history_file, trend_file = build_history(
    start_date,
    end_date
)

export_history(
    history_file,
    trend_file,
    frequency
)

print(
    "\nProcess completed successfully."
)
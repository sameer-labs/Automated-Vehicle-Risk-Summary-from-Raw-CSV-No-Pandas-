import csv
import os
import numpy as np

DATA_PATH = os.path.join("data", "car_prices.csv")
OUTPUT_PATH = os.path.join("output", "risk_summary.txt")

years = []
odometers = []
prices = []

# ------------------------
# LOAD & CLEAN DATA
# ------------------------

with open(DATA_PATH, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        try:
            year = int(row["year"])
            odometer = float(row["odometer"])
            price = float(row["sellingprice"])

            # Basic sanity checks
            if year > 1900 and odometer >= 0 and price > 0:
                years.append(year)
                odometers.append(odometer)
                prices.append(price)

        except (ValueError, KeyError):
            # Skip bad rows
            continue

total_cars = len(prices)

# Convert to numpy arrays
years = np.array(years)
odometers = np.array(odometers)
prices = np.array(prices)

# ------------------------
# RISK THRESHOLDS
# ------------------------

high_price_threshold = np.percentile(prices, 90)
high_mileage_threshold = np.percentile(odometers, 90)
old_vehicle_threshold = np.percentile(years, 10)

high_price_count = np.sum(prices >= high_price_threshold)
high_mileage_count = np.sum(odometers >= high_mileage_threshold)
old_vehicle_count = np.sum(years <= old_vehicle_threshold)

def pct(count):
    return round((count / total_cars) * 100, 2)

# ------------------------
# WRITE REPORT
# ------------------------

os.makedirs("output", exist_ok=True)

with open(OUTPUT_PATH, "w") as f:
    f.write("AUTOMATED VEHICLE RISK SUMMARY REPORT\n")
    f.write("=" * 42 + "\n\n")

    f.write(f"Total vehicles analyzed: {total_cars}\n\n")

    f.write("High Price Risk:\n")
    f.write(f"- Vehicles affected: {high_price_count}\n")
    f.write(f"- Percentage of total: {pct(high_price_count)}%\n\n")

    f.write("High Mileage Risk:\n")
    f.write(f"- Vehicles affected: {high_mileage_count}\n")
    f.write(f"- Percentage of total: {pct(high_mileage_count)}%\n\n")

    f.write("Old Vehicle Risk:\n")
    f.write(f"- Vehicles affected: {old_vehicle_count}\n")
    f.write(f"- Percentage of total: {pct(old_vehicle_count)}%\n\n")

print("Risk summary report generated successfully.")
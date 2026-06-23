from src.preprocess import *
from src.features import *

df = load_data(
    "data/ferry_data.csv"
)

df = clean_data(df)

df = create_features(df)

df = calculate_oli(df)

df = detect_idle_capacity(df)

print("\n===== NEW FEATURES =====")

print(
    df[
        [
            "Timestamp",
            "Sales Count",
            "Redemption Count",
            "Total Activity Load",
            "Redemption Pressure Ratio",
            "OLI",
            "Idle Capacity"
        ]
    ].head()
)
print("\n===== LOAD STATISTICS =====")

print(
    df["Total Activity Load"].describe()
)

print(
    "\nMaximum Load:",
    df["Total Activity Load"].max()
)
from src.analytics import *

kpis = calculate_kpis(df)

print("\n===== KPI RESULTS =====")

for key, value in kpis.items():
    print(f"{key}: {value}")
    df = add_time_segments(df)
    print("\n===== WEEKDAY VS WEEKEND =====")

print(
    df.groupby(
        "Is Weekend"
    )["Total Activity Load"]
    .mean()
)
print("\n===== SEASONAL LOAD =====")

print(
    df.groupby(
        "Season"
    )["Total Activity Load"]
    .mean()
)
print("\n===== PERIOD LOAD =====")

print(
    df.groupby(
        "Period"
    )["Total Activity Load"]
    .mean()
)
from src.analytics import *

print("\n===== TOP CONGESTION =====")

print(
    top_congestion_periods(df)
)

print("\n===== TOP IDLE =====")

print(
    top_idle_periods(df)
)

print("\n===== YEARLY LOAD =====")

print(
    yearly_load(df)
)
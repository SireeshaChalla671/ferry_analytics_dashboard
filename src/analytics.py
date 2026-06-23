import pandas as pd


# ==========================
# KPI CALCULATIONS
# ==========================

def calculate_kpis(df):

    capacity_utilization = round(
        df["OLI"].mean() * 100,
        2
    )

    congestion_pressure = round(
        (
            df["Congestion Flag"]
            .mean()
        ) * 100,
        2
    )

    idle_capacity = round(
        (
            df["Idle Capacity"]
            .mean()
        ) * 100,
        2
    )

    variability_score = round(
        df["Total Activity Load"]
        .std(),
        2
    )

    return {

        "Capacity Utilization Ratio":
            capacity_utilization,

        "Congestion Pressure Index":
            congestion_pressure,

        "Idle Capacity Percentage":
            idle_capacity,

        "Operational Variability Score":
            variability_score
    }


# ==========================
# TOP CONGESTION
# ==========================

def top_congestion_periods(
    df,
    n=20
):

    return (
        df.sort_values(
            "Total Activity Load",
            ascending=False
        )
        [
            [
                "Timestamp",
                "Sales Count",
                "Redemption Count",
                "Total Activity Load"
            ]
        ]
        .head(n)
    )


# ==========================
# TOP IDLE
# ==========================

def top_idle_periods(
    df,
    n=20
):

    return (
        df.sort_values(
            "Total Activity Load"
        )
        [
            [
                "Timestamp",
                "Sales Count",
                "Redemption Count",
                "Total Activity Load"
            ]
        ]
        .head(n)
    )


# ==========================
# WEEKDAY VS WEEKEND
# ==========================

def weekend_analysis(df):

    return (
        df.groupby(
            "Is Weekend"
        )
        [
            "Total Activity Load"
        ]
        .mean()
        .reset_index()
    )


# ==========================
# SEASON ANALYSIS
# ==========================

def seasonal_analysis(df):

    return (
        df.groupby(
            "Season"
        )
        [
            "Total Activity Load"
        ]
        .mean()
        .reset_index()
    )


# ==========================
# PERIOD ANALYSIS
# ==========================

def period_analysis(df):

    return (
        df.groupby(
            "Period"
        )
        [
            "Total Activity Load"
        ]
        .mean()
        .reset_index()
    )


# ==========================
# YEARLY TREND
# ==========================

def yearly_trend(df):

    return (
        df.groupby(
            "Year"
        )
        [
            "Total Activity Load"
        ]
        .mean()
        .reset_index()
    )


# ==========================
# AGGREGATION
# ==========================

def aggregate_data(
    df,
    granularity
):

    temp = df.copy()

    if granularity == "Hourly":

        temp = (
            temp
            .set_index(
                "Timestamp"
            )
            .resample("H")
            .agg({
                "Sales Count":"sum",
                "Redemption Count":"sum",
                "Total Activity Load":"sum"
            })
            .reset_index()
        )

    elif granularity == "Daily":

        temp = (
            temp
            .set_index(
                "Timestamp"
            )
            .resample("D")
            .agg({
                "Sales Count":"sum",
                "Redemption Count":"sum",
                "Total Activity Load":"sum"
            })
            .reset_index()
        )

    return temp


# ==========================
# EXECUTIVE SUMMARY
# ==========================

def executive_summary(df):

    avg_load = round(
        df["Total Activity Load"]
        .mean(),
        2
    )

    max_load = int(
        df["Total Activity Load"]
        .max()
    )

    idle_pct = round(
        (
            df["Idle Capacity"]
            .mean()
        ) * 100,
        2
    )

    summary = f"""
Average Activity Load : {avg_load}

Maximum Observed Load : {max_load}

Idle Capacity Percentage : {idle_pct}%

The analysis indicates notable seasonal
and temporal demand fluctuations.
Resource allocation should prioritize
high-demand periods while reducing
deployment during sustained
low-utilization intervals.
"""

    return summary


# ==========================
# RECOMMENDATIONS
# ==========================

def recommendations(df):

    recs = []

    weekend_load = (
        df[
            df["Is Weekend"]
        ]
        [
            "Total Activity Load"
        ]
        .mean()
    )

    weekday_load = (
        df[
            ~df["Is Weekend"]
        ]
        [
            "Total Activity Load"
        ]
        .mean()
    )

    if weekend_load > weekday_load:

        recs.append(
            "Increase ferry frequency during weekends."
        )

    summer_load = (
        df[
            df["Season"]
            ==
            "Summer"
        ]
        [
            "Total Activity Load"
        ]
        .mean()
    )

    winter_load = (
        df[
            df["Season"]
            ==
            "Winter"
        ]
        [
            "Total Activity Load"
        ]
        .mean()
    )

    if summer_load > winter_load * 2:

        recs.append(
            "Increase staffing and vessel allocation during summer."
        )

    idle_pct = (
        df["Idle Capacity"]
        .mean()
    )

    if idle_pct > 0.50:

        recs.append(
            "Review off-peak schedules to reduce operational costs."
        )

    if len(recs) == 0:

        recs.append(
            "Current operations appear balanced."
        )

    return recs
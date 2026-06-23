import numpy as np


def create_features(df):
    """
    Create operational analytics features
    """

    # Total Activity Load
    df["Total Activity Load"] = (
        df["Sales Count"]
        +
        df["Redemption Count"]
    )

    # Redemption Pressure Ratio
    df["Redemption Pressure Ratio"] = (
        df["Redemption Count"]
        /
        (df["Sales Count"] + 1)
    )

    # Date Parts
    df["Year"] = (
        df["Timestamp"]
        .dt.year
    )

    df["Month"] = (
        df["Timestamp"]
        .dt.month
    )

    df["Day"] = (
        df["Timestamp"]
        .dt.day
    )

    df["Hour"] = (
        df["Timestamp"]
        .dt.hour
    )

    df["Weekday"] = (
        df["Timestamp"]
        .dt.day_name()
    )

    return df


def calculate_oli(df):
    """
    Operational Load Index (0-1)
    """

    min_load = (
        df["Total Activity Load"]
        .min()
    )

    max_load = (
        df["Total Activity Load"]
        .max()
    )

    df["OLI"] = (
        (
            df["Total Activity Load"]
            -
            min_load
        )
        /
        (
            max_load
            -
            min_load
        )
    )

    return df


def detect_idle_capacity(df):
    """
    Detect low-utilization intervals
    """

    threshold = (
        df["Total Activity Load"]
        .mean()
        * 0.30
    )

    df["Idle Capacity"] = (
        df["Total Activity Load"]
        < threshold
    )

    return df


def add_time_segments(df):
    """
    Weekend, Season,
    Morning/Afternoon/Evening
    """

    # Weekend flag
    df["Is Weekend"] = (
        df["Timestamp"]
        .dt.dayofweek >= 5
    )

    # Season
    def season(month):

        if month in [12, 1, 2]:
            return "Winter"

        elif month in [3, 4, 5]:
            return "Spring"

        elif month in [6, 7, 8]:
            return "Summer"

        return "Fall"

    df["Season"] = (
        df["Month"]
        .apply(season)
    )

    # Day Period
    def period(hour):

        if hour < 12:
            return "Morning"

        elif hour < 18:
            return "Afternoon"

        return "Evening"

    df["Period"] = (
        df["Hour"]
        .apply(period)
    )

    return df


def create_congestion_flags(df):
    """
    Top 5% busiest intervals
    """

    threshold = (
        df["Total Activity Load"]
        .quantile(0.95)
    )

    df["Congestion Flag"] = (
        df["Total Activity Load"]
        > threshold
    )

    return df
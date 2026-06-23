import pandas as pd


def load_data(path):
    """
    Load ferry dataset
    """

    df = pd.read_csv(path)

    return df


def clean_data(df):
    """
    Data cleaning pipeline
    """

    # Convert timestamp
    df["Timestamp"] = pd.to_datetime(
        df["Timestamp"],
        errors="coerce"
    )

    # Remove invalid timestamps
    df = df.dropna(
        subset=["Timestamp"]
    )

    # Remove duplicates
    df = df.drop_duplicates()

    # Ensure counts are numeric
    df["Sales Count"] = pd.to_numeric(
        df["Sales Count"],
        errors="coerce"
    )

    df["Redemption Count"] = pd.to_numeric(
        df["Redemption Count"],
        errors="coerce"
    )

    # Replace missing counts
    df["Sales Count"] = (
        df["Sales Count"]
        .fillna(0)
    )

    df["Redemption Count"] = (
        df["Redemption Count"]
        .fillna(0)
    )

    # Remove negative values
    df["Sales Count"] = (
        df["Sales Count"]
        .clip(lower=0)
    )

    df["Redemption Count"] = (
        df["Redemption Count"]
        .clip(lower=0)
    )

    # Sort chronologically
    df = df.sort_values(
        "Timestamp"
    )

    df = df.reset_index(
        drop=True
    )

    return df


def filter_date_range(
    df,
    start_date,
    end_date
):
    """
    Filter dataset by date range
    """

    filtered_df = df[
        (
            df["Timestamp"].dt.date
            >= start_date
        )
        &
        (
            df["Timestamp"].dt.date
            <= end_date
        )
    ]

    return filtered_df
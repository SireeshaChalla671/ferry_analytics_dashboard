import plotly.express as px
import plotly.graph_objects as go


# ==================================
# CAPACITY UTILIZATION TIMELINE
# ==================================

def utilization_timeline(df):

    fig = px.line(
        df,
        x="Timestamp",
        y="Total Activity Load",
        title="Capacity Utilization Timeline"
    )

    fig.update_layout(
        height=500,
        xaxis_title="Time",
        yaxis_title="Activity Load"
    )

    return fig


# ==================================
# SEASONAL UTILIZATION
# ==================================

def seasonal_chart(df):

    seasonal = (
        df.groupby("Season")
        ["Total Activity Load"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        seasonal,
        x="Season",
        y="Total Activity Load",
        title="Seasonal Utilization Analysis"
    )

    fig.update_layout(
        height=500
    )

    return fig


# ==================================
# WEEKDAY VS WEEKEND
# ==================================

def weekend_chart(df):

    weekend = (
        df.groupby("Is Weekend")
        ["Total Activity Load"]
        .mean()
        .reset_index()
    )

    weekend["Is Weekend"] = (
        weekend["Is Weekend"]
        .replace({
            False: "Weekday",
            True: "Weekend"
        })
    )

    fig = px.bar(
        weekend,
        x="Is Weekend",
        y="Total Activity Load",
        title="Weekday vs Weekend Load"
    )

    fig.update_layout(
        height=500
    )

    return fig


# ==================================
# MORNING / AFTERNOON / EVENING
# ==================================

def period_chart(df):

    period = (
        df.groupby("Period")
        ["Total Activity Load"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        period,
        x="Period",
        y="Total Activity Load",
        title="Time of Day Analysis"
    )

    fig.update_layout(
        height=500
    )

    return fig


# ==================================
# YEARLY TREND
# ==================================

def yearly_trend_chart(df):

    yearly = (
        df.groupby("Year")
        ["Total Activity Load"]
        .mean()
        .reset_index()
    )

    fig = px.line(
        yearly,
        x="Year",
        y="Total Activity Load",
        markers=True,
        title="Yearly Capacity Utilization Trend"
    )

    fig.update_layout(
        height=500
    )

    return fig


# ==================================
# CONGESTION HEATMAP
# ==================================

def congestion_heatmap(df):

    heatmap_data = (
        df.pivot_table(
            values="Total Activity Load",
            index="Weekday",
            columns="Hour",
            aggfunc="mean"
        )
    )

    fig = px.imshow(
        heatmap_data,
        title="Congestion Heatmap"
    )

    fig.update_layout(
        height=600
    )

    return fig


# ==================================
# MONTHLY TREND
# ==================================

def monthly_trend_chart(df):

    monthly = (
        df.groupby("Month")
        ["Total Activity Load"]
        .mean()
        .reset_index()
    )

    fig = px.line(
        monthly,
        x="Month",
        y="Total Activity Load",
        markers=True,
        title="Monthly Utilization Trend"
    )

    fig.update_layout(
        height=500
    )

    return fig


# ==================================
# OLI DISTRIBUTION
# ==================================

def oli_distribution(df):

    fig = px.histogram(
        df,
        x="OLI",
        nbins=50,
        title="Operational Load Index Distribution"
    )

    fig.update_layout(
        height=500
    )

    return fig
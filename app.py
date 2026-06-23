import streamlit as st
import pandas as pd

from src.preprocess import *
from src.features import *
from src.analytics import *
from src.visuals import *

# ==================================
# PAGE CONFIG
# ==================================

st.set_page_config(
    page_title="Ferry Capacity Analytics",
    page_icon="🚢",
    layout="wide"
)

# ==================================
# CUSTOM CSS
# ==================================

st.markdown("""
<style>

.main-title {
    font-size: 40px;
    font-weight: bold;
    color: #003366;
}

.subtitle {
    font-size:18px;
    color: #666666;
}

.kpi-card {
    background-color:#f7f9fc;
    padding:15px;
    border-radius:10px;
    border-left:6px solid #003366;
}

</style>
""", unsafe_allow_html=True)

# ==================================
# HEADER
# ==================================

st.markdown(
    '<div class="main-title">🚢 Ferry Capacity Utilization & Operational Efficiency Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Toronto Ferry Operations Analytics Dashboard</div>',
    unsafe_allow_html=True
)

st.divider()

# ==================================
# LOAD DATA
# ==================================

@st.cache_data
def load_pipeline():

    df = load_data(
        "data/ferry_data.csv"
    )

    df = clean_data(df)

    df = create_features(df)

    df = calculate_oli(df)

    df = detect_idle_capacity(df)

    df = add_time_segments(df)

    df = create_congestion_flags(df)

    return df


df = load_pipeline()

# ==================================
# SIDEBAR
# ==================================

st.sidebar.header("Filters")

start_date = st.sidebar.date_input(
    "Start Date",
    df["Timestamp"].min().date()
)

end_date = st.sidebar.date_input(
    "End Date",
    df["Timestamp"].max().date()
)

season_filter = st.sidebar.multiselect(
    "Season",
    options=sorted(df["Season"].unique()),
    default=sorted(df["Season"].unique())
)

granularity = st.sidebar.selectbox(
    "Granularity",
    [
        "15 Minute",
        "Hourly",
        "Daily"
    ]
)

# ==================================
# APPLY FILTERS
# ==================================

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

filtered_df = filtered_df[
    filtered_df["Season"]
    .isin(season_filter)
]

# ==================================
# KPI CALCULATIONS
# ==================================

kpis = calculate_kpis(filtered_df)

# ==================================
# KPI ROW
# ==================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Capacity Utilization %",
    kpis["Capacity Utilization Ratio"]
)

col2.metric(
    "Congestion Pressure %",
    kpis["Congestion Pressure Index"]
)

col3.metric(
    "Idle Capacity %",
    kpis["Idle Capacity Percentage"]
)

col4.metric(
    "Variability Score",
    kpis["Operational Variability Score"]
)

st.divider()

# ==================================
# TABS
# ==================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📊 Executive Overview",
        "🚢 Utilization",
        "🔥 Congestion",
        "💤 Idle Capacity",
        "📈 Trends & Recommendations"
    ]
)

# ==================================
# TAB 1
# ==================================

with tab1:

    st.subheader(
        "Executive Summary"
    )

    st.info(
        executive_summary(
            filtered_df
        )
    )

    st.subheader(
        "Seasonal Utilization"
    )

    st.plotly_chart(
        seasonal_chart(
            filtered_df
        ),
        use_container_width=True
    )

# ==================================
# TAB 2
# ==================================

with tab2:

    st.subheader(
        "Capacity Utilization Timeline"
    )

    st.plotly_chart(
        utilization_timeline(
            filtered_df
        ),
        use_container_width=True
    )

    st.subheader(
        "Operational Load Distribution"
    )

    st.plotly_chart(
        oli_distribution(
            filtered_df
        ),
        use_container_width=True
    )

# ==================================
# TAB 3
# ==================================

with tab3:

    st.subheader(
        "Congestion Heatmap"
    )

    st.plotly_chart(
        congestion_heatmap(
            filtered_df
        ),
        use_container_width=True
    )

    st.subheader(
        "Top Congested Intervals"
    )

    st.dataframe(
        top_congestion_periods(
            filtered_df
        )
    )

# ==================================
# TAB 4
# ==================================

with tab4:

    st.subheader(
        "Top Idle Intervals"
    )

    st.dataframe(
        top_idle_periods(
            filtered_df
        )
    )

    st.subheader(
        "Weekend vs Weekday"
    )

    st.plotly_chart(
        weekend_chart(
            filtered_df
        ),
        use_container_width=True
    )

# ==================================
# TAB 5
# ==================================

with tab5:

    st.subheader(
        "Time of Day Analysis"
    )

    st.plotly_chart(
        period_chart(
            filtered_df
        ),
        use_container_width=True
    )

    st.subheader(
        "Yearly Trend"
    )

    st.plotly_chart(
        yearly_trend_chart(
            filtered_df
        ),
        use_container_width=True
    )

    st.subheader(
        "Monthly Trend"
    )

    st.plotly_chart(
        monthly_trend_chart(
            filtered_df
        ),
        use_container_width=True
    )

    st.subheader(
        "Operational Recommendations"
    )

    for rec in recommendations(
        filtered_df
    ):
        st.success(rec)

# ==================================
# DOWNLOAD SECTION
# ==================================

st.divider()

st.subheader(
    "Export Analysis Data"
)

csv = filtered_df.to_csv(
    index=False
)

st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name="ferry_analysis.csv",
    mime="text/csv"
)

# ==================================
# FOOTER
# ==================================

st.caption(
    "Ferry Capacity Utilization & Operational Efficiency Analytics System"
)
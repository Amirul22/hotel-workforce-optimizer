import streamlit as st
import pandas as pd
import joblib

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Hotel Workforce & GOP Optimizer",
    layout="wide"
)

st.title("🏨 Hotel Workforce & GOP Optimizer")

# =====================================================
# LOAD MODEL
# =====================================================

model = joblib.load("labor_model.pkl")

# =====================================================
# TABS
# =====================================================

tab1, tab2 = st.tabs(
    [
        "Forecast Dashboard",
        "Upload Hotel Data"
    ]
)

# =====================================================
# TAB 1 - FORECAST
# =====================================================

with tab1:

    st.header("Forecast Drivers")

    col1, col2, col3 = st.columns(3)

    with col1:

        occupancy = st.number_input(
            "Occupancy %",
            min_value=0.0,
            max_value=100.0,
            value=85.0
        )

        adr = st.number_input(
            "ADR ($)",
            value=320.0
        )

    with col2:

        rooms_revenue = st.number_input(
            "Rooms Revenue ($)",
            value=75000.0
        )

        fb_revenue = st.number_input(
            "F&B Revenue ($)",
            value=30000.0
        )

    with col3:

        covers = st.number_input(
            "Covers",
            value=600
        )

    if st.button("Generate Forecast"):

        # ========================
        # MODEL FORECAST
        # ========================

        input_data = pd.DataFrame({
            "Occupancy": [occupancy],
            "ADR": [adr],
            "Rooms_Revenue": [rooms_revenue],
            "FB_Revenue": [fb_revenue],
            "Covers": [covers]
        })

        predicted_hours = model.predict(
            input_data
        )[0]

        payroll = predicted_hours * 38.5

        total_revenue = (
            rooms_revenue +
            fb_revenue
        )

        payroll_percent = (
            payroll /
            total_revenue
        ) * 100

        revenue_per_hour = (
            total_revenue /
            predicted_hours
        )

        other_costs = (
            total_revenue * 0.35
        )

        gop = (
            total_revenue
            - payroll
            - other_costs
        )

        # ========================
        # EXEC DASHBOARD
        # ========================

        st.header("Executive Dashboard")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Revenue",
            f"${total_revenue:,.0f}"
        )

        c2.metric(
            "Payroll",
            f"${payroll:,.0f}"
        )

        c3.metric(
            "Payroll %",
            f"{payroll_percent:.1f}%"
        )

        c4.metric(
            "Forecast GOP",
            f"${gop:,.0f}"
        )

        st.divider()

        c5, c6, c7 = st.columns(3)

        c5.metric(
            "Labor Hours",
            f"{predicted_hours:.0f}"
        )

        c6.metric(
            "Revenue / Labor Hour",
            f"${revenue_per_hour:,.0f}"
        )

        c7.metric(
            "ADR",
            f"${adr:,.0f}"
        )

        # ========================
        # DEPARTMENT HOURS
        # ========================

        housekeeping_hours = (
            occupancy * 5.6
        )

        front_office_hours = (
            occupancy * 1.3
        )

        kitchen_hours = (
            covers * 0.34
        )

        restaurant_hours = (
            covers * 0.55
        )

        bar_hours = (
            covers * 0.22
        )

        st.header(
            "Department Hours Forecast"
        )

        department_hours = pd.DataFrame({
            "Department": [
                "Housekeeping",
                "Front Office",
                "Kitchen",
                "Restaurant",
                "Bars"
            ],
            "Hours": [
                round(housekeeping_hours),
                round(front_office_hours),
                round(kitchen_hours),
                round(restaurant_hours),
                round(bar_hours)
            ]
        })

        st.dataframe(
            department_hours,
            use_container_width=True
        )

        st.bar_chart(
            department_hours.set_index(
                "Department"
            )
        )

        # ========================
        # DEPARTMENT PAYROLL
        # ========================

        hk_payroll = (
            housekeeping_hours * 34
        )

        fo_payroll = (
            front_office_hours * 42
        )

        kitchen_payroll = (
            kitchen_hours * 39
        )

        restaurant_payroll = (
            restaurant_hours * 36
        )

        bar_payroll = (
            bar_hours * 37
        )

        st.header(
            "Department Payroll Forecast"
        )

        payroll_df = pd.DataFrame({
            "Department": [
                "Housekeeping",
                "Front Office",
                "Kitchen",
                "Restaurant",
                "Bars"
            ],
            "Payroll": [
                round(hk_payroll),
                round(fo_payroll),
                round(kitchen_payroll),
                round(restaurant_payroll),
                round(bar_payroll)
            ]
        })

        st.dataframe(
            payroll_df,
            use_container_width=True
        )

        st.bar_chart(
            payroll_df.set_index(
                "Department"
            )
        )

# =====================================================
# TAB 2 - DATA UPLOAD
# =====================================================

with tab2:

    st.header(
        "Upload Hotel Payroll Data"
    )

    uploaded_file = st.file_uploader(
        "Upload CSV",
        type=["csv"]
    )

    if uploaded_file is not None:

        df = pd.read_csv(
            uploaded_file
        )

        st.success(
            f"Loaded {len(df):,} records"
        )

        st.subheader(
            "Preview"
        )

        st.dataframe(df.head())

        st.subheader(
            "Columns"
        )

        st.write(
            list(df.columns)
        )

        st.subheader(
            "Summary Statistics"
        )

        st.dataframe(
            df.describe()
        )

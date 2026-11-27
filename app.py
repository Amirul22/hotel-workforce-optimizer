import streamlit as st
import pandas as pd
import joblib

# --------------------------
# Page Setup
# --------------------------

st.set_page_config(
    page_title="Hotel Workforce Optimizer",
    layout="wide"
)

st.title("🏨 Hotel Workforce & GOP Optimizer")

# --------------------------
# Load Model
# --------------------------

model = joblib.load("labor_model.pkl")

# --------------------------
# Inputs
# --------------------------

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
    restaurant_covers = st.number_input(
        "Restaurant Covers",
        value=420
    )

    bar_covers = st.number_input(
        "Bar Covers",
        value=180
    )

# --------------------------
# Forecast Button
# --------------------------

if st.button("Generate Forecast"):

    total_covers = (
        restaurant_covers +
        bar_covers
    )

    input_data = pd.DataFrame({
        'Occupancy': [occupancy],
        'ADR': [adr],
        'Rooms_Revenue': [rooms_revenue],
        'FB_Revenue': [fb_revenue],
        'Covers': [total_covers]
    })

    predicted_hours = model.predict(
        input_data
    )[0]

    # --------------------------
    # Department Hours
    # --------------------------

    housekeeping_hours = occupancy * 5.6

    front_office_hours = occupancy * 1.3

    restaurant_hours = (
        restaurant_covers * 0.55
    )

    bar_hours = (
        bar_covers * 0.40
    )

    kitchen_hours = (
        restaurant_covers +
        bar_covers
    ) * 0.34

    total_department_hours = (
        housekeeping_hours +
        front_office_hours +
        restaurant_hours +
        bar_hours +
        kitchen_hours
    )

    # --------------------------
    # Hourly Rates
    # --------------------------

    hk_rate = 34
    fo_rate = 42
    restaurant_rate = 36
    bar_rate = 37
    kitchen_rate = 39

    # --------------------------
    # Department Payroll
    # --------------------------

    hk_payroll = housekeeping_hours * hk_rate

    fo_payroll = front_office_hours * fo_rate

    restaurant_payroll = (
        restaurant_hours *
        restaurant_rate
    )

    bar_payroll = (
        bar_hours *
        bar_rate
    )

    kitchen_payroll = (
        kitchen_hours *
        kitchen_rate
    )

    total_payroll = (
        hk_payroll +
        fo_payroll +
        restaurant_payroll +
        bar_payroll +
        kitchen_payroll
    )

    # --------------------------
    # Finance Metrics
    # --------------------------

    total_revenue = (
        rooms_revenue +
        fb_revenue
    )

    payroll_percent = (
        total_payroll /
        total_revenue
    ) * 100

    revenue_per_hour = (
        total_revenue /
        total_department_hours
    )

    other_costs = (
        total_revenue * 0.35
    )

    gop = (
        total_revenue -
        total_payroll -
        other_costs
    )

    # --------------------------
    # Executive Summary
    # --------------------------

    st.header("Executive Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Revenue",
        f"${total_revenue:,.0f}"
    )

    c2.metric(
        "Payroll",
        f"${total_payroll:,.0f}"
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
        "ML Labor Hours",
        f"{predicted_hours:.0f}"
    )

    c6.metric(
        "Total Dept Hours",
        f"{total_department_hours:.0f}"
    )

    c7.metric(
        "Revenue / Labor Hour",
        f"${revenue_per_hour:.0f}"
    )

    # --------------------------
    # Department Forecast
    # --------------------------

    st.header("Department Hours Forecast")

    dept_hours = pd.DataFrame({
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
        dept_hours,
        use_container_width=True
    )

    # --------------------------
    # Department Payroll
    # --------------------------

    st.header("Department Payroll Forecast")

    payroll_df = pd.DataFrame({
        "Department": [
            "Housekeeping",
            "Front Office",
            "Kitchen",
            "Restaurant",
            "Bars"
        ],
        "Payroll ($)": [
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
import streamlit as st
import joblib

model = joblib.load("labor_model.pkl")

st.title("🏨 Hotel Workforce Optimizer")

occupancy = st.number_input("Occupancy", value=85)
adr = st.number_input("ADR", value=320)
rooms_revenue = st.number_input("Rooms Revenue", value=75000)
fb_revenue = st.number_input("F&B Revenue", value=30000)
covers = st.number_input("Covers", value=400)

if st.button("Forecast"):

    prediction = model.predict(
        [[occupancy, adr,
          rooms_revenue,
          fb_revenue,
          covers]]
    )[0]

    payroll = prediction * 38.5

    st.metric(
        "Forecast Labor Hours",
        f"{prediction:.0f}"
    )

    st.metric(
        "Forecast Payroll",
        f"${payroll:,.0f}"
    )

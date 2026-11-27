
import streamlit as st
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

# ====================================================
# PAGE CONFIG
# ====================================================

st.set_page_config(
    page_title="Hotel Workforce Intelligence Platform",
    layout="wide"
)

st.title("🏨 Hotel Workforce Intelligence Platform")

# ====================================================
# SIDEBAR SCENARIO DRIVERS
# ====================================================

st.sidebar.header("Scenario Planning")

occupancy = st.sidebar.slider(
    "Occupancy %",
    40,
    100,
    85
)

adr = st.sidebar.slider(
    "ADR ($)",
    150,
    600,
    320
)

rooms_revenue = st.sidebar.number_input(
    "Rooms Revenue",
    value=80000
)

fb_revenue = st.sidebar.number_input(
    "F&B Revenue",
    value=35000
)

restaurant_covers = st.sidebar.number_input(
    "Restaurant Covers",
    value=450
)

bar_covers = st.sidebar.number_input(
    "Bar Covers",
    value=180
)

# ====================================================
# TABS
# ====================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Executive Dashboard",
    "Workforce Forecast",
    "Scenario Planning",
    "GOP Optimizer",
    "Upload & Train"
])

# ====================================================
# MODEL STORAGE
# ====================================================

if "models_trained" not in st.session_state:
    st.session_state.models_trained = False

# ====================================================
# TAB 5 - DATA UPLOAD & TRAINING
# ====================================================

with tab5:

    st.header("Upload Workforce Dataset")

    uploaded_file = st.file_uploader(
        "Upload hotel_workforce_dataset.csv",
        type=["csv"]
    )

    if uploaded_file:

        df = pd.read_csv(uploaded_file)

        st.success(
            f"Loaded {len(df):,} rows"
        )

        st.dataframe(df.head())

        # ---------------------------
        # Housekeeping Model
        # ---------------------------

        X_hk = df[
            ["Occupancy"]
        ]

        y_hk = df["HK_Hours"]

        hk_model = RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )

        hk_model.fit(X_hk, y_hk)

        # ---------------------------
        # Front Office Model
        # ---------------------------

        y_fo = df["FO_Hours"]

        fo_model = RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )

        fo_model.fit(X_hk, y_fo)

        # ---------------------------
        # Kitchen Model
        # ---------------------------

        X_fb = df[
            [
                "FB_Revenue",
                "Restaurant_Covers",
                "Bar_Covers"
            ]
        ]

        kitchen_model = RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )

        kitchen_model.fit(
            X_fb,
            df["Kitchen_Hours"]
        )

        restaurant_model = RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )

        restaurant_model.fit(
            X_fb,
            df["Restaurant_Hours"]
        )

        bar_model = RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )

        bar_model.fit(
            X_fb,
            df["Bar_Hours"]
        )

        st.session_state.hk_model = hk_model
        st.session_state.fo_model = fo_model
        st.session_state.kitchen_model = kitchen_model
        st.session_state.restaurant_model = restaurant_model
        st.session_state.bar_model = bar_model

        st.session_state.models_trained = True

        st.success(
            "Department Models Trained Successfully"
        )

# ====================================================
# FORECASTS
# ====================================================

if st.session_state.models_trained:

    hk_hours = st.session_state.hk_model.predict(
        [[occupancy]]
    )[0]

    fo_hours = st.session_state.fo_model.predict(
        [[occupancy]]
    )[0]

    fb_inputs = [[
        fb_revenue,
        restaurant_covers,
        bar_covers
    ]]

    kitchen_hours = (
        st.session_state.kitchen_model
        .predict(fb_inputs)[0]
    )

    restaurant_hours = (
        st.session_state.restaurant_model
        .predict(fb_inputs)[0]
    )

    bar_hours = (
        st.session_state.bar_model
        .predict(fb_inputs)[0]
    )

else:

    hk_hours = occupancy * 5.5
    fo_hours = occupancy * 1.4
    kitchen_hours = restaurant_covers * 0.30
    restaurant_hours = restaurant_covers * 0.45
    bar_hours = bar_covers * 0.50

# ====================================================
# COSTS
# ====================================================

hk_rate = 34
fo_rate = 42
kitchen_rate = 39
restaurant_rate = 36
bar_rate = 37

rooms_hours = hk_hours + fo_hours

fb_hours = (
    kitchen_hours +
    restaurant_hours +
    bar_hours
)

rooms_labor_cost = (
    hk_hours * hk_rate +
    fo_hours * fo_rate
)

fb_labor_cost = (
    kitchen_hours * kitchen_rate +
    restaurant_hours * restaurant_rate +
    bar_hours * bar_rate
)

total_labor_hours = (
    rooms_hours +
    fb_hours
)

total_payroll = (
    rooms_labor_cost +
    fb_labor_cost
)

total_revenue = (
    rooms_revenue +
    fb_revenue
)

payroll_pct = (
    total_payroll /
    total_revenue
) * 100

other_costs = (
    total_revenue * 0.35
)

gop = (
    total_revenue -
    total_payroll -
    other_costs
)

# ====================================================
# EXEC DASHBOARD
# ====================================================

with tab1:

    st.header("Executive Dashboard")

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Revenue",
        f"${total_revenue:,.0f}"
    )

    c2.metric(
        "Labor Hours",
        f"{total_labor_hours:,.0f}"
    )

    c3.metric(
        "Payroll",
        f"${total_payroll:,.0f}"
    )

    c4.metric(
        "Payroll %",
        f"{payroll_pct:.1f}%"
    )

    c5.metric(
        "Forecast GOP",
        f"${gop:,.0f}"
    )

# ====================================================
# WORKFORCE FORECAST
# ====================================================

with tab2:

    workforce_df = pd.DataFrame({
        "Department":[
            "Housekeeping",
            "Front Office",
            "Kitchen",
            "Restaurant",
            "Bars"
        ],
        "Hours":[
            round(hk_hours),
            round(fo_hours),
            round(kitchen_hours),
            round(restaurant_hours),
            round(bar_hours)
        ]
    })

    st.dataframe(
        workforce_df,
        use_container_width=True
    )

# ====================================================
# SCENARIO PLANNING
# ====================================================

with tab3:

    st.metric(
        "Revenue per Labor Hour",
        f"${total_revenue / total_labor_hours:,.0f}"
    )

    st.write(
        "Adjust the sliders in the sidebar to test different scenarios."
    )

# ====================================================
# GOP OPTIMIZER
# ====================================================

with tab4:

    target_payroll_pct = st.slider(
        "Target Payroll %",
        20.0,
        40.0,
        28.0
    )

    target_payroll = (
        total_revenue *
        target_payroll_pct
    ) / 100

    savings_required = (
        total_payroll -
        target_payroll
    )

    optimized_gop = (
        total_revenue -
        target_payroll -
        other_costs
    )

    improvement = (
        optimized_gop - gop
    )

    if savings_required > 0:

        st.error(
            f"Payroll exceeds target by ${savings_required:,.0f}"
        )

    else:

        st.success(
            "Payroll is below target"
        )

    st.metric(
        "Optimized GOP",
        f"${optimized_gop:,.0f}"
    )

    st.metric(
        "GOP Improvement",
        f"${improvement:,.0f}"
    )

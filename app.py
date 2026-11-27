
import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="Hotel Workforce Optimizer",
    layout="wide"
)

st.title("🏨 Hotel Workforce Optimizer")

uploaded_file = st.file_uploader(
    "Upload Hotel Payroll Data",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.success(
        f"Loaded {len(df):,} records"
    )

    st.subheader("Data Preview")

    st.dataframe(df.head())

    st.subheader("Columns")

    st.write(list(df.columns))

model = joblib.load("labor_model.pkl")

occupancy = st.number_input(
    "Occupancy %",
    value=85.0
)

adr = st.number_input(
    "ADR",
    value=320.0
)

rooms_revenue = st.number_input(
    "Rooms Revenue",
    value=75000.0
)

fb_revenue = st.number_input(
    "F&B Revenue",
    value=30000.0
)

covers = st.number_input(
    "Covers",
    value=400
)

if st.button("Forecast"):

    prediction = model.predict(
        pd.DataFrame({
            "Occupancy":[occupancy],
            "ADR":[adr],
            "Rooms_Revenue":[rooms_revenue],
            "FB_Revenue":[fb_revenue],
            "Covers":[covers]
        })
    )[0]

    payroll = prediction * 38.5

    st.metric(
        "Labor Hours",
        f"{prediction:.0f}"
    )

    st.metric(
        "Payroll",
        f"${payroll:,.0f}"
    )

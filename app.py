
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

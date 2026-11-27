
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

# Rest of your app code...

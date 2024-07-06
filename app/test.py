import streamlit as st
import pandas as pd

uploaded_file = st.file_uploader(
    "Upload your CSV, XLS, or XLXS file", type=["csv", "xlsx"], accept_multiple_files=False, key="uploaded_file"
)

if uploaded_file is not None:
    uploaded_file_name = str(uploaded_file.name)

    display_csv = pd.read_csv(uploaded_file)
    display_csv.columns = display_csv.columns.str.strip()  # Strip any leading/trailing spaces
    st.dataframe(display_csv)  # Display the uploaded CSV file for verification

    if st.button("Calculate Profitability"):
        st.write(uploaded_file_name)

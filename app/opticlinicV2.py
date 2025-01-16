import streamlit as st
import pandas as pd

# App header
st.header("Welcome to OptiClinic")
st.text("Please choose your desired calculator")
url = "https://docs.google.com/document/d/1QYCh_ro920zFCjdyPP-N9XR0l_IdOMQawnz_P2HfI60/edit?usp=sharing"
st.write("Check out this [guide](%s)" % url)
st.write("Try out this Test CSV file for the Excel Calculator!")

# Example template data for download
TEMPLATEDATA = """Office,Dentist,Anesthesiologist,Patient ID,Procedure Type,Procedure Duration (mins),Turnover Time (mins),Procedure Fee ($),Total Cost (Staff, Anesthesia),Expected Income ($)
1,Dr. A,Dr. X,P001,Complex,60,15,1500,600,900
1,Dr. B,Dr. Y,P002,Simple,30,10,800,400,400
1,Dr. A,Dr. X,P003,Simple,30,15,800,400,400
2,Dr. C,Dr. Z,P004,Complex,90,20,1800,700,1100
2,Dr. D,Dr. W,P005,Simple,45,15,1000,500,500
"""

st.download_button('Download Test CSV', TEMPLATEDATA, file_name='template_file.csv')

# Set up calculator tabs
ExcelCalculator, BasicCalculator = st.tabs(["ExcelCalculator", "BasicCalculator"])

# Class to handle the productivity calculations
class ProductivityCalculator:
    def __init__(self, data):
        self.data = data

    # Total daily time includes procedure duration and turnover time
    def total_daily_time(self):
        procedure_duration_col = self._get_column_by_partial_name("Procedure Duration")
        turnover_time_col = self._get_column_by_partial_name("Turnover Time")
        return self.data[procedure_duration_col].sum() + self.data[turnover_time_col].sum()

    # Total production based on procedure fee
    def total_daily_production(self):
        procedure_fee_col = self._get_column_by_partial_name("Procedure Fee")
        return self.data[procedure_fee_col].sum()

    # Total cost involves staff and anesthesia
    def total_cost(self):
        total_cost_col = self._get_column_by_partial_name("Total Cost")
        return self.data[total_cost_col].sum()

    # Expected income is computed based on the provided column
    def expected_income(self):
        expected_income_col = self._get_column_by_partial_name("Expected Income")
        return self.data[expected_income_col].sum()

    # Profitability as difference between production and cost
    def profitability(self):
        return self.total_daily_production() - self.total_cost()

    # Helper function to dynamically fetch column by partial match
    def _get_column_by_partial_name(self, partial_name):
        matches = [col for col in self.data.columns if partial_name in col]
        if matches:
            return matches[0]
        else:
            st.error(f"Column with partial name '{partial_name}' not found.")
            st.stop()

    # Report generation
    def print_report(self):
        st.write(f"Total Daily Time: {self.total_daily_time()} minutes")
        st.write(f"Total Daily Production: ${self.total_daily_production()}")
        st.write(f"Total Cost (Staff, Anesthesia): ${self.total_cost()}")
        st.write(f"Expected Income: ${self.expected_income()}")
        st.write(f"Profitability: ${self.profitability()}")

# Excel Calculator tab: handles CSV/XLS file uploads and calculations
with ExcelCalculator:  
    st.header("Efficiency calculator for optimization")
    uploaded_file = st.file_uploader("Upload your CSV, XLS, or XLSX file", type=["csv", "xlsx"], accept_multiple_files=False, key="uploaded_file")

    if uploaded_file is not None:
        uploaded_file_name = str(uploaded_file.name)

        # If CSV file is uploaded, read and display it
        if uploaded_file_name.endswith(".csv"):
            display_data = pd.read_csv(uploaded_file)
            st.dataframe(display_data)  # Display the uploaded CSV file for verification

            if st.button("Calculate Profitability"):
                calculator = ProductivityCalculator(display_data)
                calculator.print_report()
        
        # If Excel file is uploaded, read and display it
        elif uploaded_file_name.endswith(".xlsx"):
            display_data = pd.read_excel(uploaded_file)
            st.dataframe(display_data)

            if st.button("Calculate Profitability"):
                calculator = ProductivityCalculator(display_data)
                calculator.print_report()
        
        # Handle incorrect file types
        else:
            st.header("Invalid file type. Please upload a .csv or .xlsx file")

# Basic Calculator for manual input values
with BasicCalculator:
    st.header("Basic calculator for manual input")

    # Manual input fields for calculating based on user input
    cases_per_day = st.number_input("Enter cases per day")
    avg_production_per_case = st.number_input("Enter average production per case ($)")
    avg_time_per_case = st.number_input("Enter average time per case (minutes)")
    tat_between_cases = st.number_input("Turnaround time between cases (minutes)")
    total_fees_anesthesia = st.number_input("Enter total fees charged for anesthesia ($)")

    if st.button("Calculate"):
        total_time = cases_per_day * (avg_time_per_case + tat_between_cases)
        total_production = cases_per_day * avg_production_per_case
        profitability = total_production - total_fees_anesthesia

        st.write(f"Total Daily Time: {total_time} minutes")
        st.write(f"Total Daily Production: ${total_production}")
        st.write(f"Profitability: ${profitability}")

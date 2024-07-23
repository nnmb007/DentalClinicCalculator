import streamlit as st
import pandas as pd
from io import StringIO

st.header("Welcome to noah")
st.text("Please choose your desired calculator")
url = "https://docs.google.com/document/d/1QYCh_ro920zFCjdyPP-N9XR0l_IdOMQawnz_P2HfI60/edit?usp=sharing"
st.write("Check out this [guide](%s)" % url)
st.write("Try out this Test CSV file for the Excel Calculator!")

TEMPLATEDATA = """dental_provider,anesthesia_provider,time_spent,anesthesia_fee,number_of_assistant,cases_per_day,tat_between_cases,production_per_case,overtime_minutes
Dr X,,20,,0,7,10,200,3
Dr Y,Dr Z,20,300,1,7,8,500,5
Dr X,,20,,2,7,15,200,12
Dr X,,20,,1,7,20,200,1
Dr Y,,20,,1,7,12,200,6
Dr X,,17,,1,7,16,200,3
    """

st.download_button('Download Test CSV', TEMPLATEDATA, file_name='template_file.csv')
ExcelCalculator, BasicCalculator = st.tabs(["ExcelCalculator", "BasicCalculator"])

with ExcelCalculator:  
    st.header("Efficiency calculator for optimization")
    uploaded_file = st.file_uploader(
        "Upload your CSV, XLS, or XLXS file", type=["csv", "xlsx"], accept_multiple_files=False, key="uploaded_file"
    )

    class ProductivityCalculator:
        def __init__(
            self,
            cases_per_day,
            avg_production_per_case,
            avg_time_per_case,
            tat_between_cases,
            total_fees_anesthesia,
            total_overtime_minutes
            # anesthesia_provider,
            # dental_provider,
            # assistants,
        ):
            self.cases_per_day = cases_per_day
            self.avg_production_per_case = avg_production_per_case
            self.avg_time_per_case = avg_time_per_case
            self.tat_between_cases = tat_between_cases
            self.total_fees_anesthesia = total_fees_anesthesia
            self.total_overtime_minutes = total_overtime_minutes
            # self.anesthesia_provider = anesthesia_provider
            # self.dental_provider = dental_provider
            # self.assistants = assistants

        def total_daily_time(self):
            total_case_time = self.cases_per_day * self.avg_time_per_case
            total_tat_time = (self.cases_per_day - 1) * self.tat_between_cases
            return total_case_time + total_tat_time

        def total_daily_production(self):
            return (self.cases_per_day * self.avg_production_per_case)

        def profitability(self):
            total_daily_production = self.total_daily_production()
            return total_daily_production - self.total_fees_anesthesia / ((self.cases_per_day * self.avg_time_per_case) + (self.cases_per_day - 1 * self.tat_between_cases))

        def print_report(self):
            st.write(f"Cases per Day: {self.cases_per_day}")
            # st.write(f"Average Production per Case: ${self.avg_production_per_case}")
            st.write(f"Average Time per Case: {self.avg_time_per_case} minutes")
            st.write(f"Average Turnaround Time Between Cases: {self.tat_between_cases} minutes")
            st.write(f"Total Fees for Anesthesia: ${self.total_fees_anesthesia}")
            st.write(f"Total Daily Time: {self.total_daily_time()} minutes")
            st.write(f"Total Daily Production: ${self.total_daily_production()}")
            st.write(f"Profitability: ${round(self.profitability(), 2)} per hour")
            st.write(f"Total Overtime in minutes: {self.total_overtime_minutes} minutes")
            
    if uploaded_file is not None:
        uploaded_file_name = str(uploaded_file.name)
        if uploaded_file_name.find(".csv") > 0:
            display_csv = pd.read_csv(uploaded_file)
            st.dataframe(display_csv)  # Display the uploaded CSV file for verification

            if st.button("Calculate Profitability"):
                calculator = ProductivityCalculator(
                    display_csv["cases_per_day"].mean(),
                    display_csv["production_per_case"].mean(),
                    display_csv["time_spent"].mean(),
                    display_csv["tat_between_cases"].mean(),
                    display_csv["anesthesia_fee"].sum(),
                    display_csv["overtime_minutes"].sum(),  
                )
                calculator.print_report()
        elif uploaded_file_name.find(".xls") > 0:
            display_excel = pd.read_excel(uploaded_file)
            st.dataframe(display_excel)

            if st.button("Calculate Profitability"):
                calculator = ProductivityCalculator(
                    display_excel["cases_per_day"].mean(),
                    display_excel["production_per_case"].mean(),
                    display_excel["time_spent"].mean(),
                    display_excel["tat_between_cases"].mean(),
                    display_excel["anesthesia_fee"].sum(),
                    display_excel["overtime_minutes"].sum(),  
                )
                calculator.print_report()
        else:
            st.header("WRONG TYPE UPLOADED: DO .csv, .xls, or .xlsx")
with BasicCalculator:
    st.header("Welcome to the basic calculator")

    class ProductivityCalculator:
        def __init__(
            self,
            cases_per_day,
            avg_production_per_case,
            avg_time_per_case,
            tat_between_cases,
            total_fees_anesthesia,
            anesthesia_provider,
            dental_provider,
            assistants,
        ):
            self.cases_per_day = cases_per_day
            self.avg_production_per_case = avg_production_per_case
            self.avg_time_per_case = avg_time_per_case
            self.tat_between_cases = tat_between_cases
            self.total_fees_anesthesia = total_fees_anesthesia
            self.anesthesia_provider = anesthesia_provider
            self.dental_provider = dental_provider
            self.assistants = assistants

        def total_daily_time(self):
            total_case_time = self.cases_per_day * self.avg_time_per_case
            total_tat_time = (self.cases_per_day - 1) * self.tat_between_cases
            return total_case_time + total_tat_time

        def total_daily_production(self):
            return self.cases_per_day * self.avg_production_per_case

        def profitability(self):
            total_daily_production = self.total_daily_production()
            return total_daily_production - self.total_fees_anesthesia / ((self.cases_per_day * self.avg_time_per_case) + (self.cases_per_day - 1 * self.tat_between_cases))


        def print_report(self):
            st.write(f"Total Daily Time: {self.total_daily_time()} minutes")
            st.write(f"Total Daily Production: ${self.total_daily_production()}")
            st.write(f"Total Fees for Anesthesia: ${self.total_fees_anesthesia}")
            st.write(f"Profitability: ${round(self.profitability(), 2)} per hour")
    cases_per_day = st.number_input("Enter cases per day")
    avg_production_per_case = st.number_input("Enter Average production per case ($)")
    avg_time_per_case = st.number_input("Enter Avg time per case (minutes)")
    tat_between_cases = st.number_input("Turnaround time between cases (minutes)")
    total_fees_anesthesia = st.number_input("Enter Total Fees charged for anesthesia ($)")
    anesthesia_provider = st.text_input("Enter Anesthesia Provider", "")
    dental_provider = st.text_input("Enter dental provider", "")
    assistants = st.text_input("Enter the assistants")
    #overtime = st.text_input ("Enter the amount of overtime")

    if st.button("Calculate"):
        calculator = ProductivityCalculator(
            cases_per_day,
            avg_production_per_case,
            avg_time_per_case,
            tat_between_cases,
            total_fees_anesthesia,
            anesthesia_provider,
            dental_provider,
            assistants,
        )
        calculator.print_report()
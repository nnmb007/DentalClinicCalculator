# Import command
import streamlit as st

class ProductivityCalculator:
    def __init__(self, cases_per_day, avg_production_per_case, avg_time_per_case, tat_between_cases, total_fees_anesthesia, anesthesia_provider, dental_provider, assistants):
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
        return total_daily_production - self.total_fees_anesthesia

    def print_report(self):
        st.write(f"Total Daily Time: {self.total_daily_time()} minutes")
        st.write(f"Total Daily Production: ${self.total_daily_production()}")
        st.write(f"Total Fees for Anesthesia: ${self.total_fees_anesthesia}")
        st.write(f"Profitability: ${self.profitability()}")


cases_per_day = 7
avg_production_per_case = st.number_input("Enter Average production per case")
avg_time_per_case  = st.number_input("Enter Avg time per case")
tat_between_cases = st.number_input("Turnaround time between cases")
total_fees_anesthesia =  st.number_input("Enter Total Fees charged for anesthesia")
anesthesia_provider = st.text_input("Enter Anesthesia Provider", "")
dental_provider = st.text_input("Enter dental provider", "")
assistants = st.text_input("Enter the assistants")

if(st.button("Calculate Profitability")):
    calculator = ProductivityCalculator(cases_per_day, avg_production_per_case, avg_time_per_case, tat_between_cases, total_fees_anesthesia, anesthesia_provider, dental_provider, assistants)
    calculator.print_report()
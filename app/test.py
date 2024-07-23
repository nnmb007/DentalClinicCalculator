import streamlit as st

# Text files
with open('bookcsv.csv', 'rb') as f:
   st.download_button('Download CSV', f, file_name='testfile.csv')
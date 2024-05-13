import os
import streamlit as st
import pandas as pd

def do(directory, csv_file):
    # Load the selected CSV file
    csv_path = os.path.join(directory, csv_file)
    quiz_df = pd.read_csv(csv_path)
    
    st.write(csv_path)
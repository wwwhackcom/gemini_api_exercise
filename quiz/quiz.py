import os
import random
import streamlit as st
import pandas as pd

def do(directory, category):
    # Load the selected CSV file
    csv_file = f"{category}.csv"
    csv_path = os.path.join(directory, csv_file)
    quiz_df = pd.read_csv(csv_path)
    
    # Display the question
    get_question(quiz_df)

def get_question(df):
    # Randomly select a question from the DataFrame
    index = random.randint(0, len(df) - 1)
    st.divider()
    st.markdown(f"<h6 style='text-align: left; color: black;'>Question: {df.loc[index, 'Questions']}</h6>", unsafe_allow_html=True)
    st.divider()
    options = ['A', 'B', 'C', 'D']
    for i, option in enumerate(options, start=1):
        if not pd.isnull(df.loc[index, option]):
            st.markdown(f"***{chr(64+i)}: {df.loc[index, option]}***")

import os
import random
import streamlit as st
import pandas as pd

def do(directory, category):
    # Load the selected CSV file
    csv_file = f"{category}.csv"
    csv_path = os.path.join(directory, csv_file)
    quiz_df = pd.read_csv(csv_path)
    
    # Randomly select a question from the DataFrame
    random_index = random.randint(0, len(quiz_df) - 1)

    # Display the question
    get_question(random_index, quiz_df)

def get_question(index, df):    
    st.write(df.loc[index, 'Questions'])
    options = ['A', 'B', 'C', 'D']
    for i, option in enumerate(options, start=1):
        st.write(f"{chr(64+i)}: {df.loc[index, option]}")

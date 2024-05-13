import os
import streamlit as st
from quiz import quiz

def entry():
    # Call the function with the path to your CSV directory
    display_files_in_directory('quiz/csv/')

def display_files_in_directory(directory):
    # List all files in the directory
    files = os.listdir(directory)
    
    # Filter for CSV files
    categories = [file[:-4] for file in files if file.endswith('.csv')]

    st.header("Ice Breaker: Quiz!")
    st.subheader("A collection of trivia, multiple choice questions and answers!")
    st.divider()
    st.markdown("**Please select a category:**")

    selected_category = st.selectbox('', categories)

    # Display CSV files
    if selected_category:
        # Load the selected CSV file
        quiz.do(directory, selected_category)
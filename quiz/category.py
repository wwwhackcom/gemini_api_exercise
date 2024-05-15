import os
import streamlit as st
from quiz import quiz

def entry():
    # Call the function with the path to your CSV directory
    display_categories()

#@st.cache_data
def display_files_in_directory(directory):
    # List all files in the directory
    files = os.listdir(directory)
    
    # Filter for CSV files
    categories = [file[:-4] for file in files if file.endswith('.csv')]
    return categories

def display_categories():
    directory = 'quiz/csv/'
    categories = display_files_in_directory(directory)
    st.header("Ice Breaker: Quiz!")
    st.subheader("A collection of trivia, multiple choice questions and answers!")
    st.divider()
    st.markdown("**Please select a category:**")

    selected_category = st.selectbox('', categories)

    # Display CSV files
    if selected_category:
        # Load the selected CSV file
        quiz.do(directory, selected_category)
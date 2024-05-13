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
    csv_files = [file for file in files if file.endswith('.csv')]
    
    # Display CSV files
    for csv_file in csv_files:
        if st.button(os.path.splitext(csv_file)[0]):
            # Load the selected CSV file
            quiz.do(directory, csv_file)
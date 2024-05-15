import os
import random
import streamlit as st
import pandas as pd

#@st.cache_data
def load_data(directory, category):
    # Load the selected CSV file
    csv_file = f"{category}.csv"
    csv_path = os.path.join(directory, csv_file)
    df = pd.read_csv(csv_path)
    if "current_quiz" in st.session_state:
        del st.session_state["current_quiz"]
    return df

def do(directory, category):
    # Load the selected CSV file
    quiz_df = load_data(directory, category)
    
    # Initialize session state
    if "user_answers" not in st.session_state:
        st.session_state["user_answers"] = []

    if "current_index" not in st.session_state:
        st.session_state["current_index"] = 0

    if "current_count" not in st.session_state:
        st.session_state["current_count"] = 1
    
    if "correct_count" not in st.session_state:
        st.session_state["correct_count"] = 0

    if "current_quiz" not in st.session_state:
        st.session_state["current_quiz"] = get_question(quiz_df)
        
    display_question(st.session_state["current_quiz"])
    if st.button('Next'):
        st.session_state["current_index"] += 1
        st.session_state["current_count"] += 1
        st.session_state["current_quiz"] = get_question(quiz_df) 
            
    st.write(f"Your current quiz score: {st.session_state["correct_count"]}/{st.session_state["current_count"]}")

def get_question(df):
    #index = random.randint(0, len(df) - 1)
    index = st.session_state["current_index"]
    question = df.loc[index, 'Questions']
    options_labels = ['A', 'B', 'C', 'D']
    options = [f"{label}. {df.loc[index, label]}" for label in options_labels if not pd.isnull(df.loc[index, label])]
    answer = df.loc[index, 'Correct']
    return {"question": question, "options": options, "correct_answer": answer}

def display_question(quiz):
    with st.form("quiz_form", clear_on_submit = True):
        st.markdown(f"<h6 style='text-align: left; color: black;'>Question: {quiz["question"]}</h6>", unsafe_allow_html=True)

        st.text_input("Answer:", key="input_answer")
        st.form_submit_button(label="Submit", on_click=check_answer, kwargs={"current_quiz": quiz})
        display_options(quiz)
    
def check_answer(current_quiz):
    input_answer = st.session_state["input_answer"].strip()
    is_correct = input_answer.lower() == current_quiz["correct_answer"].lower()
    if is_correct:
        st.success(f"{input_answer} is correct!", icon="✅")
        st.session_state["correct_count"] += 1
    else:
        st.error(f"{input_answer} is incorrect!", icon="❌")

def display_options(current_quiz):
    for option in current_quiz["options"]:
        st.write(f"***{option}***")
    
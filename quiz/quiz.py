import os
import sys
sys.path.insert(0, '..')
import random
import streamlit as st
import pandas as pd
import generativeai as api

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
    quiz_df = load_data(directory, category)
    
    # Initialize session state
    if "user_answers" not in st.session_state:
        st.session_state["user_answers"] = []

    if "current_index" not in st.session_state:
        st.session_state["current_index"] = get_index(quiz_df)

    if "current_count" not in st.session_state:
        st.session_state["current_count"] = 1
    
    if "correct_count" not in st.session_state:
        st.session_state["correct_count"] = 0


    if st.button('Next'):
        st.session_state["current_index"] = get_index(quiz_df)
        st.session_state["current_count"] += 1

    quiz = get_question(quiz_df)
    display_question(quiz)

    if st.button("Gemini's Hint"):
        response = use_gemini(quiz, True)
        st.write(f"AI Response: {response}")

    if st.button("Gemini's Answer: 0-shot"):
        response = use_gemini(quiz)
        st.write(f"AI Response: {response}")

    st.write(f"Your current quiz score: {st.session_state['correct_count']}/{st.session_state['current_count']}")

def get_index(df):
    #return st.session_state.setdefault("current_index", 0) + 1
    return random.randint(0, len(df) - 1)

def get_question(df):
    index = st.session_state["current_index"]
    if index >= len(df):
        index = 0
    question = df.iloc[index]['Questions']
    options_labels = ['A', 'B', 'C', 'D']
    options = [f"{label}. {df.loc[index, label]}" for label in options_labels if not pd.isnull(df.loc[index, label])]
    answer = df.loc[index, 'Correct']
    return {"question": question, "options": options, "correct_answer": answer}

def display_question(quiz):
    use_ai = st.checkbox("AI check: few-shot", key="use_ai")
    with st.form("quiz_form", clear_on_submit = True):
        st.markdown(f"<h6 style='text-align: left; color: black;'>Question: {quiz['question']}</h6>", unsafe_allow_html=True)

        st.text_input("Answer:", key="input_answer")
        st.form_submit_button(label="Submit", on_click=check_answer, kwargs={"current_quiz": quiz})
        display_options(quiz)
    
def check_answer(current_quiz):
    input_answer = st.session_state["input_answer"].strip()
    if st.session_state["use_ai"]:
        is_correct = check_with_gemini(current_quiz["question"], current_quiz["options"], input_answer)
    else:
        is_correct = input_answer.lower() == current_quiz["correct_answer"].lower()
    if is_correct:
        st.success(f"{input_answer} is correct!", icon="✅")
        st.session_state["correct_count"] += 1
    else:
        st.error(f"{input_answer} is incorrect!", icon="❌")

def display_options(current_quiz):
    for option in current_quiz["options"]:
        st.write(f"***{option}***")
    
def use_gemini(current_quiz, hint_only = False):
    prompt = f"question is {current_quiz['question']}, and options are {current_quiz['options']}"
    if hint_only:
        prompt += ", please give short explanation but not the answer."
    else:
        prompt += ", please give the answer and explanation."
    return api.generate_response(prompt)

def check_with_gemini(question, options, input_answer):
    prompt = (
        "What is the accuracy of the given answer to the given question.\n" +
        "Always start the response with '{score}/10', explain the answer afterwards.\n" +
        "When evaluating answers, ignore case sensitive.\n" +
        "Examples\n" +
        "Question: Which of these animals swims the fastest?\n" +
        "Options: A. Flounder; B. Shark; C. Dolphin; D. Jellyfish\n" +  
        "Answer: Dolphin\n" + 
        "Response: 10/10\n" + 
        "The answer is correct since Dolphins are known for their speed can be up to 56 kilometers per hour in short bursts.!\n" +
        "Question: These are the least painful parts of the body to put a tattoo on.\n" +
        "Options: A. The shoulders; B. The ankles; C. Fleshy parts of the arms and legs; D. The belly and the calf\n" +  
        "Answer: The shoulders\n" + 
        "Response: 3/10\n" +
        "The answer is not correct since shoulders areas have more nerves and bones, which can make the tattooing process more painful.\n" +
        "Question: " + question + "\n" +
        "Options: " + '; '.join(options) + "\n" +  
        "Answer: " + input_answer + "\n"
        "Response:"
    )
    #st.info(prompt, icon="🤖")
    response = api.generate_response(prompt)
    st.info(response, icon="🤖")
    score = int((response.split("\n")[0]).split("/")[0])
    is_correct = score>=9
    return is_correct

import streamlit as st
from quiz import category

PAGES = {
    "Quiz": category
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

page = PAGES[selection]

# Display
page.entry()
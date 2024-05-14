import streamlit as st
from streamlit_option_menu import option_menu
from quiz import category
import settings

PAGES = {
    "Ice breaker": category,
    "Settings": settings
}

with st.sidebar:
    selected = option_menu("Navigation", ["Ice breaker", 'Settings'], 
        icons=['house', 'gear'], menu_icon="cast", default_index=0)

page = PAGES[selected]
# Display
page.entry()
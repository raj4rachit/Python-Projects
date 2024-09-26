# Import convention
import streamlit as st
from streamlit_extras.bottom_container import bottom

def example():
    st.write("This is the main container")

    with bottom():
        st.write("This is the bottom container")
        st.text_input("This is a text input in the bottom container")
import streamlit as st
from PIL import Image

class WELCOME:
    def welcome(self):
        st.markdown("""
        # Welcome to Pharmaceutical Drug Discovery Intelligent System!

        A platform to assist your drug discovery journey to discover novel drugs.

        """)
        image1 = Image.open('doctor.png')
        st.image(image1, use_column_width=True)

        st.markdown("""
        # We provide you the best solution to get the insights on the drug candidates.

        """)
        image2 = Image.open('experiment.png')
        st.image(image2, use_column_width=True)

        st.markdown("""
        # We create an advance machine learning system to make your drug discovery process faster.

        """)
        image3 = Image.open('robot.jpg')
        st.image(image3, use_column_width=True)

        st.markdown("""
        # Molecules effectiveness analysis on drug target inhibition now has become easier!

        """)
        image4 = Image.open('medicine.jpg')
        st.image(image4, use_column_width=True)
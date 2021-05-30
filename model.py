import streamlit as st
import pandas as pd
import pickle
from download import Download

dw = Download()

class Model:
    def build_model(self, input_data):
        load_model = pickle.load(open('acetylcholinesterase_model.pkl', 'rb'))
        prediction = load_model.predict(input_data)
        st.header('**Prediction output**')
        prediction_output = pd.Series(prediction, name='pIC50')
        molecule_name = pd.Series(load_data[1], name='molecule_name')
        df = pd.concat([molecule_name, prediction_output], axis=1)
        st.write(df)
        st.markdown(dw.filedownload(df), unsafe_allow_html=True)
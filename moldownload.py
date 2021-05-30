import streamlit as st
import base64
from bring_value import Value

val = Value()
user_fp = val.get_value1()

class Mol_Download:
    def filedownload(self, df):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
        href = f'<a href="data:file/csv;base64,{b64}" download="descriptor_{user_fp}.csv">Download CSV File</a>'
        return href
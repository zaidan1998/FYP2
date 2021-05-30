import streamlit as st
import pandas as pd
import subprocess
import os
from moldownload import Mol_Download
from bring_value import Value

dw = Mol_Download()
val = Value()
user_fp = val.get_value1()
selected_fp = val.get_value2()

class MOL_DESC:
    def desc_calc(self):
        
        bashCommand = "java -Xms2G -Xmx2G -Djava.awt.headless=true -jar ./PaDEL-Descriptor/PaDEL-Descriptor.jar -removesalt -standardizenitro -fingerprints -descriptortypes ./PaDEL-Descriptor/%s -dir ./ -file descriptors_output.csv" % selected_fp
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        
        st.subheader('Calculated molecular descriptors')
        desc = pd.read_csv('descriptors_output.csv')
        st.write(desc)
        st.markdown(dw.filedownload(desc), unsafe_allow_html=True)
        
        nmol = desc.shape[0]
        ndesc = desc.shape[1]
        
        st.info('Number of molecules: ' + str(nmol))
        st.info('Number of descriptors: ' + str(ndesc-1))
        os.remove('molecule.smi')
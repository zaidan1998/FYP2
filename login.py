import streamlit as st
import pandas as pd
import subprocess
import os
import base64
from database import DB
from make_hash import MakeHash
from check_hash import CheckHash
from PIL import Image
from desc_calc import DESCRIPTOR
from download import Download
import pickle

db = DB()
mh = MakeHash()
ch = CheckHash()
mol = DESCRIPTOR()
dw = Download()

class LOGIN:
    def login(self):
        username = st.sidebar.text_input("Email")
        password = st.sidebar.text_input("Password",type='password')
        if st.sidebar.checkbox("Login"):
            db.create_usertable()
            hashed_pswd = mh.make_hashes(password)

            result = db.login_user(username,ch.check_hashes(password,hashed_pswd))
            if result:

                st.success("Logged In as {}".format(username))

                task = st.selectbox("Task",["Home", "Molecular Descriptor Calculator", "Bioactivity Prediction"])
                if task == "Home":
                    st.markdown("""
                    # Welcome!
                    
                    Let's get started on your research. It's now or never!
                    """)

                    image2 = Image.open('research.png')
                    st.image(image2, use_column_width=True)

                    st.markdown("""
                    Available Features:
                    
                    1. Molecular Descriptor Calculator
                    - Calculate the descriptors of molecules.
                    
                    2. Bioactivity Prediction
                    - Predict the bioactivity towards inhibiting the drug targets' enzyme.
                    """)

                elif task == "Molecular Descriptor Calculator":
                    def desc_calc():
        
                        bashCommand = "java -Xms2G -Xmx2G -Djava.awt.headless=true -jar ./PaDEL-Descriptor/PaDEL-Descriptor.jar -removesalt -standardizenitro -fingerprints -descriptortypes ./PaDEL-Descriptor/%s -dir ./ -file descriptors_output.csv" % selected_fp
                        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
                        output, error = process.communicate()
                        
                        st.subheader('Calculated molecular descriptors')
                        desc = pd.read_csv('descriptors_output.csv')
                        st.write(desc)
                        st.markdown(filedownload(desc), unsafe_allow_html=True)
                        
                        nmol = desc.shape[0]
                        ndesc = desc.shape[1]
                        st.info('Selected fingerprint: ' + user_fp)
                        st.info('Number of molecules: ' + str(nmol))
                        st.info('Number of descriptors: ' + str(ndesc-1))
                        os.remove('molecule.smi')

                    def filedownload(df):
                        csv = df.to_csv(index=False)
                        b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
                        href = f'<a href="data:file/csv;base64,{b64}" download="descriptor_{user_fp}.csv">Download CSV File</a>'
                        return href

                    st.markdown("""
                    # Molecular Descriptor Calculator

                    This feature allows you to calculate descriptors of molecules that you can use for computational drug discovery projects such as for the construction of quantitative structure-activity/property relationship (QSAR/QSPR) models.

                    In this feature we will be focusing on 12 **molecular fingerprints** (`AtomPairs2D`, `AtomPairs2DCount`, `CDK`, `CDKextended`, `CDKgraphonly`, `EState`, `KlekotaRoth`, `KlekotaRothCount`, `MACCS`, `PubChem`, `Substructure` and `SubstructureCount`).
                    
                    """)

                    with st.sidebar.header('1. Upload your CSV data'):
                        uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
                        st.sidebar.markdown("""
                    [Example CSV input file](https://raw.githubusercontent.com/dataprofessor/data/master/acetylcholinesterase_04_bioactivity_data_3class_pIC50.csv)
                    """)

                    with st.sidebar.header('2. Enter column names for 1) Molecule ID and 2) SMILES'):
                        name_mol = st.sidebar.text_input('Enter column name for Molecule ID', 'molecule_chembl_id')
                        name_smiles = st.sidebar.text_input('Enter column name for SMILES', 'canonical_smiles')

                    with st.sidebar.header('3. Set parameters'):
                        fp_dict = {'AtomPairs2D':'AtomPairs2DFingerprinter.xml',
                                'AtomPairs2DCount':'AtomPairs2DFingerprintCount.xml',
                                'CDK':'Fingerprinter.xml',
                                'CDKextended':'ExtendedFingerprinter.xml',
                                'CDKgraphonly':'GraphOnlyFingerprinter.xml',
                                'EState':'EStateFingerprinter.xml',
                                'KlekotaRoth':'KlekotaRothFingerprinter.xml',                                    'KlekotaRothCount':'KlekotaRothFingerprintCount.xml',
                                'MACCS':'MACCSFingerprinter.xml',
                                'PubChem':'PubchemFingerprinter.xml',
                                'Substructure':'SubstructureFingerprinter.xml',
                                'SubstructureCount':'SubstructureFingerprintCount.xml'}
                        user_fp = st.sidebar.selectbox('Choose fingerprint to calculate', list(fp_dict.keys()) )

                        selected_fp = fp_dict[user_fp]

                        df0 = pd.read_csv('acetylcholinesterase_04_bioactivity_data_3class_pIC50.csv')
                        all_mol = df0.shape[0]
                        number2calc = st.sidebar.slider('How many molecules to compute?', min_value=10, max_value=all_mol, value=10, step=10)

                    if uploaded_file is not None:
    
                        @st.cache
                        def load_csv():
                            csv = pd.read_csv(uploaded_file).iloc[:number2calc,1:]
                            return csv
                        df = load_csv()
                        df2 = pd.concat([df[name_smiles], df[name_mol]], axis=1)
                            
                        df2.to_csv('molecule.smi', sep = '\t', header = False, index = False)
                        st.subheader('Initial data from CSV file')
                        st.write(df)
                        st.subheader('Formatted as PADEL input file')
                        st.write(df2)
                        with st.spinner("Calculating descriptors..."):
                            desc_calc()

                    else:
                        st.info('Awaiting for CSV file to be uploaded.')
                        if st.button('Press to use Example Dataset'):
                            
                            @st.cache
                            def load_data():
                                
                                df = pd.read_csv('acetylcholinesterase_04_bioactivity_data_3class_pIC50.csv').iloc[:number2calc,1:]
                                return df
                            df = load_data()
                            df2 = pd.concat([df[name_smiles], df[name_mol]], axis=1)
                            
                            df2.to_csv('molecule.smi', sep = '\t', header = False, index = False)
                            st.subheader('Initial data from CSV file')
                            st.write(df)
                            st.subheader('Formatted as PADEL input file')
                            st.write(df2)
                            with st.spinner("Calculating descriptors..."):
                                desc_calc()



                elif task == "Bioactivity Prediction":
                    def build_model(input_data):
                        load_model = pickle.load(open('acetylcholinesterase_model.pkl', 'rb'))
                        prediction = load_model.predict(input_data)
                        st.header('**Prediction output**')
                        prediction_output = pd.Series(prediction, name='pIC50')
                        molecule_name = pd.Series(load_data[1], name='molecule_name')
                        df = pd.concat([molecule_name, prediction_output], axis=1)
                        st.write(df)
                        st.markdown(dw.filedownload(df), unsafe_allow_html=True)

                    image = Image.open('logo.png')

                    st.image(image, use_column_width=True)

                    st.markdown("""
                    # Bioactivity Prediction App (Acetylcholinesterase)

                    This app allows you to predict the bioactivity towards inhibting the `Acetylcholinesterase` enzyme. `Acetylcholinesterase` is a drug target for Alzheimer's disease.

                    """)

                    with st.header('1. Upload your CSV data'):
                        uploaded_file = st.sidebar.file_uploader("Upload your input file", type=['txt'])
                        st.markdown("""
                    [Example input file](https://raw.githubusercontent.com/dataprofessor/bioactivity-prediction-app/main/example_acetylcholinesterase.txt)
                    """)

                    if st.button('Predict'):
                        load_data = pd.read_table(uploaded_file, sep=' ', header=None)
                        load_data.to_csv('molecule.smi', sep = '\t', header = False, index = False)

                        st.header('**Original input data**')
                        st.write(load_data)

                        with st.spinner("Calculating descriptors..."):
                            mol.desc_calc()

                        st.header('**Calculated molecular descriptors**')
                        desc = pd.read_csv('descriptors_output.csv')
                        st.write(desc)
                        st.write(desc.shape)

                        st.header('**Subset of descriptors from previously built models**')
                        Xlist = list(pd.read_csv('descriptor_list.csv').columns)
                        desc_subset = desc[Xlist]
                        st.write(desc_subset)
                        st.write(desc_subset.shape)

                        build_model(desc_subset)

                    else:
                        st.info('Upload input data in the sidebar to start!')

            else:
                st.warning("Incorrect Username/Password")

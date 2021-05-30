import streamlit as st
import pandas as pd
from database import DB
from make_hash import MakeHash

db = DB()
mh = MakeHash()

class SIGNUP:
    def signup(self):
            st.subheader("Create New Account")
            new_user = st.text_input("Email")
            new_password = st.text_input("Password",type='password')

            if st.button("Signup"):
                db.create_usertable()
                db.add_userdata(new_user,mh.make_hashes(new_password))
                st.success("You have successfully created a valid Account")
                st.info("Go to Login Menu to login")
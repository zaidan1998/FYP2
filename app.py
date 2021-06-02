import streamlit as st
from multiapp import MultiApp
from login import LOGIN
from signup import SIGNUP
from welcome import WELCOME

app = MultiApp()
lg = LOGIN()
sg = SIGNUP()
wc = WELCOME()

app.add_app("Welcome", wc.welcome)
app.add_app("Log In", lg.login)
app.add_app("Sign Up", sg.signup)

app.run()
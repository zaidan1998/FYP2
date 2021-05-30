import streamlit as st
import hashlib

class MakeHash:
    def make_hashes(self, password):
        return hashlib.sha256(str.encode(password)).hexdigest()
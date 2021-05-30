import streamlit as st
import hashlib
from make_hash import MakeHash

mh = MakeHash()

class CheckHash:

    def check_hashes(self, password, hashed_text):
        if mh.make_hashes(password) == hashed_text:
            return hashed_text
        return False

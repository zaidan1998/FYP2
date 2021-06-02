import streamlit as st
import sqlite3

class DB:

    def create_usertable(self):
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

    def add_userdata(self, username,password):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
        conn.commit()

    def login_user(self, username,password):
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
        data = c.fetchall()
        return data
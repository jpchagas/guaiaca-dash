import streamlit as st
import sqlite3
import hashlib

# Initialize SQLite Database
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create user table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
''')
conn.commit()

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to add a new user
def add_user(username, password):
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hash_password(password)))
    conn.commit()

# Function to authenticate user
def authenticate_user(username, password):
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, hash_password(password)))
    return c.fetchone()

# User Registration
def register_user():
    st.subheader("Register")
    username = st.text_input("Username", key="register_username")
    password = st.text_input("Password", type="password", key="register_password")
    if st.button("Register"):
        if username and password:
            if not authenticate_user(username, password):
                add_user(username, password)
                st.success("User registered successfully!")
            else:
                st.warning("User already exists!")
        else:
            st.warning("Please enter a username and password.")

# User Login
def login_user():
    st.subheader("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        if username and password:
            user = authenticate_user(username, password)
            if user:
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.success("Logged in successfully!")
                st.experimental_rerun()
            else:
                st.error("Invalid username or password.")
        else:
            st.warning("Please enter a username and password.")

# Main Function
def main():
    st.title("Streamlit Authentication with SQLite")

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in']:
        st.write(f"Welcome, {st.session_state['username']}!")
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.experimental_rerun()
    else:
        login_user()
        st.write("---")
        register_user()

if __name__ == '__main__':
    main()

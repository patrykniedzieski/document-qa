import streamlit as st
from openai import OpenAI

# --- Dane logowania ---
USERNAME = "admin"
PASSWORD = "1234"

# --- Session state ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# --- Funkcja logowania ---
def login():
    st.title("🔐 Panel logowania")

    username = st.text_input("Login")
    password = st.text_input("Hasło", type="password")

    if st.button("Zaloguj"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.success("Zalogowano!")
            st.rerun()
        else:
            st.error("Nieprawidłowy login lub hasło")


# --- Jeśli użytkownik nie jest zalogowany ---
if not st.session_state.logged_in:
    login()
    st.stop()


# --- Logout ---
if st.button("Wyloguj"):
    st.session_state.logged_in = False
    st.rerun()


# --- APLIKACJA ---
st.title("📄 Document question answering")

st.write(
    "Upload a document below and ask a question about it – GPT will answer!"
)

openai_api_key = st.text_input("OpenAI API Key", type="password")

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    client = OpenAI(api_key=openai_api_key)

    uploaded_file = st.file_uploader(
        "Upload a document (.txt or .md)", type=("txt", "md")
    )

    question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:

        document = uploaded_file.read().decode()

        messages = [
            {
                "role": "user",
                "content": f"Here's a document: {document} \n\n---\n\n {question}",
            }
        ]

        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True,
        )

        st.write_stream(stream)

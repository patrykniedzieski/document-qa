import streamlit as st
import pandas as pd
from openai import OpenAI

# --- PROSTE LOGOWANIE ---
USERNAME = "admin"
PASSWORD = "1234"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

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

if not st.session_state.logged_in:
    login()
    st.stop()

if st.button("Wyloguj"):
    st.session_state.logged_in = False
    st.rerun()

# --- APLIKACJA ---
st.title("📄 CSV Mapping & Document QA")

# OpenAI API Key
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # --- Upload CSV ---
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Podgląd danych:", df.head())

        # --- Mapowanie kolumn ---
        price_column = st.selectbox("Wybierz kolumnę, która odpowiada za Price", df.columns)

        if st.button("Mapuj kolumnę Price"):
            df_mapped = df.copy()
            df_mapped["Price"] = df_mapped[price_column]
            st.success(f"Kolumna '{price_column}' została przypisana do 'Price'.")
            st.write(df_mapped.head())

            # Opcja zapisu
            csv = df_mapped.to_csv(index=False).encode("utf-8")
            st.download_button("Pobierz zmodyfikowany CSV", csv, "mapped.csv", "text/csv")

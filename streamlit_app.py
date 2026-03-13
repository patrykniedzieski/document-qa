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

# --- PANEL CSV & QA ---
st.title("📄 CSV Mapping + Document QA")

# --- OpenAI API Key ---
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # --- Upload CSV ---
    uploaded_csv = st.file_uploader("Upload CSV file", type=["csv"])
    df_mapped = None

    if uploaded_csv:
        # UWAGA: pliki z średnikiem
        df = pd.read_csv(uploaded_csv, sep=';')
        st.subheader("Podgląd danych źródłowych")
        st.dataframe(df.head())

        # --- Mapowanie kolumn ---
        target_attributes = ["Price", "ProductName", "Quantity"]
        column_mapping = {}
        st.subheader("Mapowanie kolumn na atrybuty docelowe")

        for attr in target_attributes:
            selected_col = st.selectbox(f"Wybierz kolumnę źródłową dla '{attr}'", df.columns, key=attr)
            column_mapping[attr] = selected_col

        if st.button("Generuj zmapowany CSV"):
            df_mapped = pd.DataFrame()
            for attr, col in column_mapping.items():
                df_mapped[attr] = df[col]
            st.success("Dane zostały zmapowane!")
            st.subheader("Podgląd zmapowanych danych")
            st.dataframe(df_mapped.head())

            csv = df_mapped.to_csv(index=False).encode("utf-8")
            st.download_button("Pobierz CSV", csv, "mapped.csv", "text/csv")

    # --- Upload dokumentu do QA ---
    uploaded_doc = st.file_uploader("Upload document (.txt or .md)", type=["txt", "md"])
    question = st.text_area(
        "Zadaj pytanie o dokument lub CSV",
        placeholder="Np. podaj średnią cenę produktów",
        disabled=not uploaded_doc and df_mapped is None
    )

    if (uploaded_doc or df_mapped is not None) and question:
        # Przygotowanie treści do GPT
        content = ""
        if uploaded_doc:
            content += uploaded_doc.read().decode() + "\n\n---\n\n"
        if df_mapped is not None:
            content += "Dane CSV:\n" + df_mapped.to_csv(index=False) + "\n\n---\n\n"

        messages = [{"role": "user", "content": f"{content} {question}"}]

        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True,
        )

        st.subheader("Odpowiedź GPT")
        st.write_stream(stream)

import streamlit as st
import pandas as pd

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

# --- Wylogowanie ---
if st.button("Wyloguj"):
    st.session_state.logged_in = False
    st.rerun()

# --- GŁÓWNY PANEL ---
st.title("📄 CSV Multi-Attribute Mapping")

# Upload CSV
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("Podgląd danych źródłowych")
    st.dataframe(df.head())

    # --- Definiowanie atrybutów docelowych ---
    target_attributes = ["Price", "ProductName", "Quantity"]  # Możesz dodać więcej
    column_mapping = {}

    st.subheader("Mapowanie kolumn na atrybuty docelowe")
    for attr in target_attributes:
        if df.columns.any():
            selected_col = st.selectbox(f"Wybierz kolumnę źródłową dla '{attr}'", df.columns, key=attr)
            column_mapping[attr] = selected_col

    # --- Mapowanie danych ---
    if st.button("Generuj CSV z mapowaniem"):
        df_mapped = pd.DataFrame()
        for attr, col in column_mapping.items():
            df_mapped[attr] = df[col]
        
        st.success("Dane zostały zmapowane!")
        st.subheader("Podgląd zmapowanych danych")
        st.dataframe(df_mapped.head())

        # --- Pobranie CSV ---
        csv = df_mapped.to_csv(index=False).encode("utf-8")
        st.download_button("Pobierz CSV", csv, "mapped.csv", "text/csv")

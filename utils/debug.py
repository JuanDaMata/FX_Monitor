import requests
import streamlit as st

def debug_api():
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"

    r = requests.get(url, timeout=10)

    st.write("STATUS:", r.status_code)
    st.code(r.text)
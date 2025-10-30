import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Project Samarth", layout="centered")

st.title("Project Samarth – An Intelligent Q&A System")
st.markdown("Ask your question below, for example: **Compare rainfall in Karnataka and Kerala.**")

question = st.text_input("Enter your question:")

if st.button("Ask"):
    if question.strip():
        try:
            response = requests.post("https://project-samarth-brcd.onrender.com/query", json={"question": question})
            if response.status_code == 200:
                data = response.json()

                st.subheader("Answer")
                st.write(data.get("answer", ""))

                if "table" in data:
                    df = pd.DataFrame(data["table"])
                    st.table(df)

                
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"Error connecting to backend: {e}")
    else:
        st.warning("Please enter a question.")

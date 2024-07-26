import streamlit as st
import requests

st.title("Query Interface")
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    files = {"file": uploaded_file.getvalue()}
    response = requests.post("http://localhost:8000/upload", files=files)
    if response.status_code == 200:
        st.success("File uploaded successfully")
    else:
        st.error("Failed to upload file")

query = st.text_area("Enter your query")

if st.button("Submit"):
    if query:
        response = requests.post("http://localhost:8000/query", json={"query": query})
        if response.status_code == 200:
            st.write("Answer:")
            st.write(response.json().get("answer", "No answer found"))
        else:
            st.error("Failed to retrieve answer")
    else:
        st.error("Query cannot be empty")

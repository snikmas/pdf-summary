from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os
from groq import Groq
import requests
import streamlit as st
import io   

load_dotenv()
API_KEY = os.getenv("API_KEY")

def get_content(file):

    if isinstance(file, io.BytesIO):
        return file
    else:
        with open(file) as f:
            return f.read()

def summarize(content, prompt):


    client = Groq(api_key = API_KEY)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{prompt}\nCONTENT: \n{content}"
            }
        ],
        model='llama-3.3-70b-versatile'
    )


    res = chat_completion.choices[0].message.content
    return res

def main():

    prompt = get_content('prompt.md')

    # reader = PdfReader("test.pdf")
    # page = reader.pages[0]
    # print(page.extract_text())


    st.title("AI Document Analyzer")
    st.subheader("Upload -> Send -> Get summary")


    with st.form(key='my_form'):

        # st.subheader("Upload your file:")
        file = st.file_uploader("Upload your file") # will get uploaded file

        submit_buttion = st.form_submit_button(label="Send")

    if submit_buttion:
        if not file:
            st.warning("Please, upload the file!")
        else:
            file_content = get_content(file)

            with st.spinner("Summarizing..."):
                res = summarize(file_content, prompt)
            
            st.header("Summary:")
            st.markdown(res)
            


if __name__ == '__main__':
    main()
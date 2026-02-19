from pypdf import PdfReader
from dotenv import load_dotenv
import os
from groq import Groq
import streamlit as st
import io   
from google.genai import Client 

EXAMPLE = 'example.md'
RULES = 'rules.md'

load_dotenv()
GROK_API_KEY = os.getenv("GROK_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


client_gemini = Client(api_key=GEMINI_API_KEY)
client_groq = Groq(api_key=GROK_API_KEY)
# odel = genai.GenerativeModel('gemini-2.5-flash') # is it okay put it there?



def extract_text(file):
    print(type(file))
    full_text = ''
    reader = PdfReader(file)

    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + '\n\n'

    
    return full_text

SYSTEM_PROMPT = ''
def summarize_grok(content, rules, example):

    SYSTEM_PROMPT = f'{rules}.\n Always follow this specific Markdown template for the output {example}'


    chat_completion = client_groq.chat.completions.create(
        messages=[
            { "role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Please summarize the following document content: {content}"
            }
        ],
        model='llama-3.3-70b-versatile'
    )


    res = chat_completion.choices[0].message.content
    return res


def summarize_gemini(content, rules, example):

    SYSTEM_PROMPT = f'RULES: {rules}.\n TEMPLATE: {example}.\n\n CONTENT:: {content}'

    try:
        res = client_gemini.models.generate_content(
            model="gemini-2.5-flash",
            contents=SYSTEM_PROMPT
        )
        return res.text
    except Exception as e:
        return f"Gemini Error: {e}"

def load_system_files():
    with open (EXAMPLE) as f:
        template_content = f.read()
    with open (RULES) as f:
        rules_content = f.read()
    return rules_content, template_content


def main():

    rules, example = load_system_files()
    

    st.title("AI Document Analyzer")
    st.subheader("Upload -> Send -> Get summary")

    with st.form(key='my_form'):

        # st.subheader("Upload your file:")
        file = st.file_uploader("Upload your file", type='pdf') # will get uploaded file

        submit_buttion = st.form_submit_button(label="Send")

    if submit_buttion:
        if not file:
            st.warning("Please, upload the file!")
        else:
            file_content = extract_text(file)

            # return
            with st.spinner("Summarizing..."):
                # res = summarize_grok(file_content, rules, example) # no tokens
                res = summarize_gemini(file_content, rules, example)
            
            st.header("Summary:")
            st.markdown(res)
            


if __name__ == '__main__':
    main()
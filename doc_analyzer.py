from dotenv import load_dotenv
import os
from groq import Groq
from google.genai import Client 

from pypdf import PdfReader
from docx import Document


EXAMPLE = 'example.md'
RULES = 'rules.md'

load_dotenv()
GROK_API_KEY = os.getenv("GROK_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")



def extract_text(file):
    full_text = ''
    file_extension = file.name.split('.')[-1]

    if file_extension == 'pdf':
        reader = PdfReader(file)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text + '\n\n'
    elif file_extension == 'docx':
        reader = Document(file)
        for paragraph in reader.paragraphs:
            text = paragraph.text
            if text:
                full_text += text + '\n\n'
    elif file_extension == 'doc': # not supported
        raise ValueError("Legacy .doc files are not supported. Please upload .docx.")
    elif file_extension == 'txt':
        full_text = file.read().decode('utf-8')
    else:
        raise ValueError(f"Unsupported file extension: {file_extension}")

    return full_text



# option 1
client_gemini = Client(api_key=GEMINI_API_KEY)
client_groq = Groq(api_key=GROK_API_KEY)

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

    SYSTEM_PROMPT = f'RULES: {rules}.\n TEMPLATE: {example}.\n\n CONTENT: {content}'

    try:
        res = client_gemini.models.generate_content(
            model="gemini-2.5-flash",
            contents=SYSTEM_PROMPT
        )
        return res.text
    except Exception as e:
        return f"Gemini Error: {e}"

@st.cache_data
def load_system_files():
    with open (EXAMPLE) as f:
        template_content = f.read()
    with open (RULES) as f:
        rules_content = f.read()
    return rules_content, template_content


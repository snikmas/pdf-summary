from pypdf import PdfReader
import doc_analyzer as da
import streamlit as st


SYSTEM_PROMPT = ''


def main():

    rules, example = da.load_system_files()
    

    st.title("AI Document Analyzer")
    st.subheader("Upload -> Send -> Get summary")

    with st.form(key='my_form'):

        # st.subheader("Upload your file:")
        file = st.file_uploader("Upload your file", type=['pdf', 'docx', 'doc', 'txt']) # will get uploaded file

        submit_buttion = st.form_submit_button(label="Send")

    if submit_buttion:
        if not file:
            st.warning("Please, upload the file!")
        else:
            file_content = da.extract_text(file)

            with st.spinner("Summarizing..."):
                st.session_state['summary'] = da.summarize_gemini(file_content, rules, example)
                # res = summarize_grok(file_content, rules, example) # no tokens
    if 'summary' in st.session_state:
        st.header("Summary:")
        st.markdown(st.session_state['summary'])
            


if __name__ == '__main__':
    main()
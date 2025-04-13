import streamlit as st
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else "your-openai-key-here"

st.set_page_config(page_title="Text Summarizer with GPT", layout="centered")
st.title("GPT-Powered Text Summarizer")
st.write("Upload a `.txt` file and let GPT summarize it for you.")

# File uploader
uploaded_file = st.file_uploader("Upload your .txt file", type=["txt"])

if uploaded_file is not None:
    file_content = uploaded_file.read().decode("utf-8")

    # display text area with uploaded content
    st.subheader("File Content")
    text_input = st.text_area("Edit text before summarizing:", value=file_content, height=300)

    # generate summary
    if st.button("Summarize with GPT"):
        with st.spinner("Generating summary..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an assistant that summarizes documents."},
                        {"role": "user", "content": f"Please summarize the following text:\n{text_input}"}
                    ]
                )
                summary = response["choices"][0]["message"]["content"]

                st.subheader("Summary")
                st.markdown(f"> {summary}")

            except Exception as e:
                st.error(f"An error occurred: {e}")
else:
    st.info("Please upload a `.txt` file to get started.")

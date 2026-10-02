import streamlit as st
import os
from src.pdf_utils import extract_text_from_pdf, clean_text, chunk_text
from src.summarize import load_model, summarize_full_text
from src.tts import text_to_speech
from src.config import CHUNK_WORD_LIMIT

st.title("DocEcho.AI")
st.write("Upload a PDF to get a summary, in text and audio form.")

@st.cache_resource
def get_model():
    return load_model()

model = get_model()

uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

if uploaded_file is not None:
    if st.button("Generate Summary"):
        with open("temp_uploaded.pdf", "wb") as f:
            f.write(uploaded_file.read())

        with st.spinner("Extracting text from PDF..."):
            raw_text = extract_text_from_pdf("temp_uploaded.pdf")
            cleaned = clean_text(raw_text)
            chunks = chunk_text(cleaned, CHUNK_WORD_LIMIT)

        with st.spinner("Generating summary..."):
            final_summary = summarize_full_text(model, chunks)

        st.subheader("Summary")
        st.write(final_summary)

        with st.spinner("Preparing audio..."):
            output_path = text_to_speech(final_summary)

        st.subheader("Audio Summary")
        st.audio(output_path)

        if os.path.exists("temp_uploaded.pdf"):
            os.remove("temp_uploaded.pdf")
else:
    st.info("Please upload a PDF to continue.")
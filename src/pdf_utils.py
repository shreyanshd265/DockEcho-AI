import pdfplumber
import re
from src.config import CHUNK_WORD_LIMIT
def extract_text_from_pdf(file_path):
    text=" "
    with pdfplumber.open(file_path) as pdf:
        for pages in pdf.pages:
            page_text=pages.extract_text()
            if(page_text):
                text=text+ page_text + " "
    return text

def clean_text(text):
    cleaned_text=re.sub(r'\s+',' ',text)
    cleaned_text=cleaned_text.strip()
    return cleaned_text

def chunk_text(cleaned_text,chunk_size):
    chunked_text=[]
    splitted_to_words=cleaned_text.split()
    size=len(splitted_to_words)
    for i in range(0,size,chunk_size):
        mid=splitted_to_words[i:i+chunk_size]
        mid_string=" ".join(mid)
        chunked_text.append(mid_string)
    return chunked_text



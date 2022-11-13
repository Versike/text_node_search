#  Importing necessery libraries/modules
from PyPDF2 import PdfReader
import os.path
import re

def extract_text_pdf(path):
    """Extracting text from pdf file by using PyPDF2 module.
    After extracted text it saved on txt file to increase perfomance.
    Return usual string."""
    text = ''
    if os.path.exists('file.txt'):
        with open('file.txt', encoding='utf-8') as f:
            text = f.read()
    else: 
        path = 'file.pdf'
        reader = PdfReader(path)
        numbers_of_text = len(reader.pages)  #  Take number of pages

        for page in range(numbers_of_text):
            text += reader.pages[page].extract_text()

        with open('file.txt','w', encoding='utf-8') as f:
            f.write(text) 
    return text

def articles_splitter(text):
    articles = []
    for match in re.findall(r'(?<=УДК \d\d\d)[\s\S]*?(?=УДК)', text):
        articles.append(clean_text(match))
    return articles

def clean_text(text):
    text=text.lower()
    regular = r'[\*+\–+\#+\№\"\-+\+\=+\?+\&\^\.+\;\,+\>+\(\)\/+\:\\+]'
    regular_url = r'(http\S+)|(www\S+)|([\w\d]+www\S+)|([\w\d]+http\S+)'
    text = re.sub(regular, '', text)
    text = re.sub(regular_url, r'URL', text)
    text = re.sub(r'(\d+\s\d+)|(\d+)',' NUM ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

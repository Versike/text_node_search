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
    split_by_UDK = re.split(r'УДК ', text)
    articles = []
    for article in range(2, len(split_by_UDK) - 1):  #  0,1 elements of array are not articles
        author = split_by_UDK[article][::-1]
        _temp = re.split(r'\d{2,3}', author)  #  has article for extract author
        author = re.findall(r'[А-ЯA-Z]\. ?[А-Я-A-Z]\.? [А-Яа-я]+', _temp[0][::-1])  #  take I.O.Familya with regex
        _temp = re.split(r'Аннотация', split_by_UDK[article + 1])
        title = re.sub(r'[^\w\s]+|[\d]+', r'', _temp[0]).replace('\n', ' ').strip()  #  regex to extract title
        _temp = _temp[1].lower()
        _temp = _temp.split(". ")
        articleText = []
        for i in _temp:
            i = " ".join(clean_text(i).split())
            if len(i) > 3:
                articleText.append(i)
        articles.append([author, title, articleText])
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

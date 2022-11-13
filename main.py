from features import *
#  Extract text from pdf file
path = 'file.pdf'
text = extract_text_pdf(path)

#  Split text at differents articles
articles = []
articles = articles_splitter(text)
print(articles[0])
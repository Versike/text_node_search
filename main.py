from features import *
from tree import *

#  Extract text from pdf file
path = 'file.pdf'
text = extract_text_pdf(path)

#  Split text at differents articles
articles = []
articles = articles_splitter(text)

#  Load config and run application
tree = Tree()
words = get_wards_from_file(text,10)

for i in range(len(words)):
    adding_text_to_tree(tree, words[i], i)

# print(f"время простого поиска {simple_search(words, 'результат'):.20f}")
# print(f"время работы метода find {find_method(words, 'результат'):.20f}")

start_time = time.time()
res = search_by_phrase(tree, "результат")
if False not in res:
    res = sequential_unification(res)
    print(f"время поиска по дереву {(time.time() - start_time):.10f}")

s = ""
while s != ".":
    inp = input(">>")
    res = search_by_phrase(tree, inp)
    if False not in res:
        res = sequential_unification(res)
        if res is not None:
            articles = structure_preparation(res)
            for article, data in articles.items():
                sentences = []
                print(preparation(words[article]))
                for number_sentences, number_word in data:
                    if number_sentences not in sentences:
                        print(f" - {words[article][2][number_sentences]}")
                        sentences.append(number_sentences)
from nltk.stem.snowball import SnowballStemmer
import pymorphy2
import time
from features import *

morph = pymorphy2.MorphAnalyzer()
stemmer = SnowballStemmer("russian")

class Node:
    def __init__(self, value):
        self.children = [] # дочерний узел
        self.value = value # значение узла
        self.is_leaf = False # является ли краем
        self.data = {}

class Tree:
    root = Node("Root_Node")
    def insert_root(self, value):
        # if self.root is None or self.root.data == data:
        #     return node
        index = 0
        for l in self.root.children:
            if l.value == value:
                return False
            if l.value < value:
                index += 1
            else:
                break
        self.root.children.insert(index, Node(value))
    def insert_word(self, word_stem, data):
        node = None
        index = 0
        let = word_stem[0]
        if len(self.root.children) != 0:
            for letter in self.root.children:
                if letter.value < let:
                    index += 1
                if letter.value == let:
                    node = letter
                    break
        else:
            self.root.children.insert(0, Node(let))
            node = self.root.children[0]
        if node is None:
            self.root.children.insert(index, Node(let))
            node = self.root.children[index]
        if len(word_stem) == 1:
            if data[0] not in node.data:
                node.data[data[0]] = dict()
                if data[1] not in node.data[data[0]]:
                    node.data[data[0]][data[1]] = [data[2]]
                else:
                    node.data[data[0]][data[1]].append(data[2])
            else:
                if data[1] not in node.data[data[0]]:
                    node.data[data[0]][data[1]] = [data[2]]
                else:
                    node.data[data[0]][data[1]].append(data[2])
        else:
            for let in word_stem[1:]:
                index = 0
                is_present = False
                for n in node.children:
                    if n.value < let:
                        index += 1
                    if n.value == let:
                        node = n
                        is_present = True
                        break
                if not is_present:
                    node.children.insert(index, Node(let))
                    node = node.children[index]
                if let == word_stem[-1]:
                    if data[0] not in node.data:
                        node.data[data[0]] = dict()
                        if data[1] not in node.data[data[0]]:
                            node.data[data[0]][data[1]] = [data[2]]
                        else:
                            node.data[data[0]][data[1]].append(data[2])
                    else:
                        if data[1] not in node.data[data[0]]:
                            node.data[data[0]][data[1]] = [data[2]]
                        else:
                            node.data[data[0]][data[1]].append(data[2])

    def search_data(self, word) -> dict:
        node = None
        for n in self.root.children:
            if word[0] == n.value:
                node = n
        if node is None:
            return False
        for letter in word[1:]:
            for n in node.children:
                if letter == n.value:
                    node = n
            if node is Node:
                return False
        return node.data

def preparation(data):
    return f"authors: {data[0]}\ntitle: {data[1]}"

def adding_text_to_tree(tree: Tree, article: list, num_article):
    for num_sentences in range(len(article[2])):
        text = article[2][num_sentences]
        text = text.split() # разбиваем предложения на токены слов
        # соеденить слова оканчивающиеся на - с след словом
        for num_word in range(len(text)):
            word = text[num_word]
            if '-' in word:
                s_words = word.split('-')
                for w in s_words:
                    if (len(w) != 0):
                        # if ld.detect_langs(word)[0].lang == "ru":
                        tree.insert_word(stemmer.stem(w),
                                         [preparation(article), word, [num_article, num_sentences, num_word]])
            else:
                # if ld.detect_langs(word)[0].lang=="ru":
                if not any(map(str.isdigit, word)):  # len(word) > 1 and not any(map(str.isdigit, word)):
                    tree.insert_word(stemmer.stem(word),
                                     [preparation(article), word, [num_article, num_sentences, num_word]])
                else:
                    tree.insert_word(word, [preparation(article), word, [num_article, num_sentences, num_word]])

def search_by_word(tree: Tree, word: str):
    imp_pos = morph.parse(word)[0].tag.POS
    data = tree.search_data(stemmer.stem(word))
    result = []

    if not data:
        return False

    for key, value in data.items():
        count = 0
        for k, v in value.items():
            if imp_pos == morph.parse(k)[0].tag.POS:
                for _ in v:
                    count += 1
        if count != 0:
            for k, v in value.items():
                sentences = []
                if imp_pos == morph.parse(k)[0].tag.POS:
                    for number_article, number_sentences, number_word in v:
                        if number_sentences not in sentences:
                            result.append([number_article, number_sentences, number_word])
    return result

def search_by_phrase(tree: Tree, phrase: str):
    result = []
    phrase = phrase.split()
    for word in phrase:
        word = word.lower()
        result.append(search_by_word_without_morph(tree, word))
    return result

def search_by_word_without_morph(tree: Tree, word: str):
    data = tree.search_data(stemmer.stem(word))
    result = []
    if not data:
        return False
    for key, value in data.items():
        count = 0
        for k, v in value.items():
            for _ in v:
                count += 1
        if count != 0:
            for k, v in value.items():
                sentences = []
                for number_article, number_sentences, number_word in v:
                    if number_sentences not in sentences:
                        result.append([number_article, number_sentences, number_word])
    return result

def sequential_unification(data: list) -> list:
    if len(data) == 0:
        return None
    result = data[0]
    for i in range(len(data) - 1):
        A = result
        B = data[i + 1]
        if len(A) == 0 or len(B) == 0:
            return None
        result = []
        for a in A:
            for b in B:
                if a[:2] == b[:2]:
                    result.append(a)
    return result

def structure_preparation(data: list) -> dict:
    articles = dict()
    for line in data:
        if line[0] not in articles:
            articles[line[0]] = [line[1:]]
        else:
            if line[1:] not in articles[line[0]]:
                articles[line[0]].append(line[1:])
    return articles

def find_method(words, word):
    start_time = time.time()
    count = 0
    for article in words:
        for sentences in article[2]:
            if sentences.find(word) != -1:
                count += 1
    return time.time() - start_time

def simple_search(words, word):
    start_time = time.time()
    count = 0
    for article in words:
        for sentences in article[2]:
            sentences = sentences.split()
            for _word in sentences:
                if _word == word:
                    count+=1
    return time.time() - start_time

def get_wards_from_file(text, k=0) -> list[list[str]]:
    articles = articles_splitter(text)
    if k != 0:
        articles = articles[:k]
    return articles
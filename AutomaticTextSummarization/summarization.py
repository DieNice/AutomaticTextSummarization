import re
from itertools import combinations

import nltk

nltk.download('stopwords')
nltk.download('wordnet')

from nltk.corpus import stopwords

import networkx as nx
from nltk.stem.snowball import RussianStemmer
from nltk.tokenize import sent_tokenize, RegexpTokenizer
from nltk.stem import WordNetLemmatizer


class Summarization:
    def similarity(self, s1, s2):
        '''Calculating the similarity of sentences.
        It is calculated as the number of words that match in sentences,
        normalized by the total length of these sentences'''
        if not len(s1) or not len(s2):
            return 0.0
        return len(s1.intersection(s2)) / (1.0 * (len(s1) + len(s2)))

    def textrank(self, text):
        '''The weights of the vertices are calculated,
        they are ordered in descending order of the weight value, and sentences corresponding to the
        first n vertices are included in the abstract, where n is the desired number of sentences in the abstract.'''
        stop_words = set(stopwords.words('russian'))
        sentences = sent_tokenize(self.preprocessing(text))
        rawsentences = sent_tokenize(text)
        tokenizer = RegexpTokenizer(r'\w+')
        lmtzr = RussianStemmer()
        # stemming
        words = [set(lmtzr.stem(word) for word in tokenizer.tokenize(sentence))
                 for sentence in sentences]
        # remove stop words
        words = [{i for i in sentence if not i in stop_words} for sentence in words]
        # lemmatization
        lemmatizer = WordNetLemmatizer()
        words = [{lemmatizer.lemmatize(i) for i in sentence} for sentence in words]
        # Set weights to ribs
        pairs = combinations(range(len(sentences)), 2)
        scores = [(i, j, self.similarity(words[i], words[j])) for i, j in pairs]
        scores = filter(lambda x: x[2], scores)

        g = nx.Graph()
        g.add_weighted_edges_from(scores)
        # Set weights to vertexes
        pr = nx.pagerank(g)

        return sorted(((i, pr[i], s) for i, s in enumerate(rawsentences) if i in pr),
                      key=lambda x: pr[x[0]], reverse=True)

    def extract(self, text, persent=50):
        '''Basic procedure. Return referat'''
        tr = self.textrank(text)
        needsen = int(len(tr) * persent / 100)
        top_n = sorted(tr[:needsen])
        return '\n'.join(x[2] for x in top_n)

    def preprocessing(slef, text):
        '''Text preprocessing'''
        text = text.lower()  # convert to lowercase
        text = re.sub(r'\d+', '', text)  # remove numbers
        # text = text.translate(str.maketrans('', '', string.punctuation))  # remove punctiaction
        return text

import random

import gensim.downloader

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize, RegexpTokenizer
from sklearn.neighbors import NearestNeighbors

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')


class LexicalChains:
    """
    A class for constructing lexical chains from a given text.

    Lexical chains are sequences of related words and concepts that capture the
    coherence and semantic relationships within the text. This class processes
    the input text, identifies relevant keywords, and groups them into chains
    based on their semantic similarity.
    """
    def __init__(self):
        self.n_sentences = -1
        self.lexical_chains = []
        self.graph = {}
        self.model = None

        self._load_embeddings_model()

    @property
    def chains(self):
        return self.lexical_chains

    def _load_embeddings_model(self):
        self.model = gensim.downloader.load('word2vec-google-news-300')

    def build_graph(self, sentences):

        for index, sent in enumerate(sentences):
            words = self.pre_process(sent, remove_punctuation=True)

            X = [self.model[word] for word in words if word in self.model.key_to_index]
            nbrs = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(X)

            distances, indices = nbrs.kneighbors(X)

            for i, (dist, ind) in enumerate(zip(distances, indices)):
                word = words[i]
                for j in ind:
                    if i == j:
                        continue
                    similar_word = words[j]

                    if str(index) not in self.graph.keys():
                        self.graph[str(index)] = {}

                    if word not in self.graph[str(index)]:
                        self.graph[str(index)][word] = []

                    if similar_word not in self.graph[str(index)][word]:
                        self.graph[str(index)][word].append(similar_word)

        print(self.graph)

    @staticmethod
    def pre_process(doc, remove_punctuation=False):

        if remove_punctuation:
            tokenizer = RegexpTokenizer(r'\w+')
            words = tokenizer.tokenize(doc)
        else:
            words = word_tokenize(doc)

        words = [word.lower() for word in words if word.lower() not in stopwords.words('english')]

        return words

    def find_path(self, index, start, end, path=[]):
        path = path + [start]
        if len(path) == end:
            return path
        for node in self.graph[index][start]:
            if node not in path:
                newpath = self.find_path(index, node, end, path)
                if newpath:
                    return newpath

    def build_lexical_chains(self, doc):
        # Initialize a list to store the lexical chains
        self.lexical_chains = []
        self.graph = {}

        # split by sentences
        sentences = sent_tokenize(doc)

        # get number of sentences in doc
        self.n_sentences = len(sentences)

        self.build_graph(sentences)

    def extract_lexical_chains(self, n=3, depth=3):
        self.lexical_chains = []
        if self.n_sentences > n:
            n = self.n_sentences

        for index in range(0, n):
            elements = list(self.graph[str(index)].keys())
            start = random.choice(elements)

            self.lexical_chains.append(self.find_path(str(index), start, depth))


if __name__ == "__main__":

    documents = [
        "This is an example document. It contains multiple sentences. Each sentence has several words.",
        "Completing all of this won't happen within the initial hundred days. It won't be accomplished in the initial"
        " thousand days either, nor during the tenure of this Administration, or even perhaps within our existence on "
        "this celestial body. Nevertheless, let's commence.",
        "The mystery of life isn't a problem to solve, but a reality to experience. Arrakis teaches the attitude of the"
        " knife - chopping off what's incomplete and saying: 'Now it's complete because it's ended here.' "
        ]

    lc = LexicalChains()
    for document in documents:
        print(10*"-")
        print(document)
        lc.build_lexical_chains(document)
        lc.extract_lexical_chains(n=3)
        print(lc.graph)
        print(lc.chains)

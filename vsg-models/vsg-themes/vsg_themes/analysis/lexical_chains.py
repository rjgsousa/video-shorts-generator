import json
import logging
import time

import gensim.downloader
import networkx as nx
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize, RegexpTokenizer
from sklearn.neighbors import NearestNeighbors

from vsg_utils.files import save_to_json_file


class ThemeLexicalChains:
    """
    A class for constructing lexical chains from a given text.

    Lexical chains are sequences of related words and concepts that capture the
    coherence and semantic relationships within the text. This class processes
    the input text, identifies relevant keywords, and groups them into chains
    based on their semantic similarity.

    Morris, J. and G. Hirst. Lexical cohesion computed by thesaural relations as an indicator of the
    structure of the text. In Computational Linguistics, 18(1):pp21-45. 1991.
    """
    def __init__(self):
        self.n_sentences = -1
        self.lexical_chains = []
        self.graphs = {}
        self.model = None
        self._load_embeddings_model()

    @property
    def chains(self):
        return self.lexical_chains

    def _load_embeddings_model(self):
        start_time = time.time()
        # todo: improve this as gensim is slow loading the model.
        logging.info("loading model...")
        self.model = gensim.downloader.load('word2vec-google-news-300')
        logging.info(f"done in {time.time() - start_time} sec.")

    def build_graph(self, sentences):

        for index, sent in enumerate(sentences):
            index_str = str(index)

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

                    if index_str not in self.graphs.keys():
                        self.graphs[index_str] = nx.DiGraph()

                    if word not in self.graphs[index_str].nodes():
                        # node does not exist - adding new one
                        self.graphs[index_str].add_node(word)

                    if similar_word not in self.graphs[index_str].neighbors(word):
                        # adds an edge from "word" to "similar word" (weighted by their distance on the embedding space)
                        # by weighting the edges will allow us to extract more relevant strongly connected edges
                        dist_norm = np.linalg.norm(dist)
                        self.graphs[index_str].add_edge(word, similar_word, weight=dist_norm)

    @staticmethod
    def pre_process(doc, remove_punctuation=False):

        if remove_punctuation:
            tokenizer = RegexpTokenizer(r'\w+')
            words = tokenizer.tokenize(doc)
        else:
            words = word_tokenize(doc)

        words = [word.lower() for word in words if word.lower() not in stopwords.words('english')]

        return words

    def build_lexical_chains(self, doc):
        # Initialize a list to store the lexical chains
        self.lexical_chains = []
        self.graphs = {}

        # split by sentences
        sentences = sent_tokenize(doc, language="english")

        # set number of sentences in doc which will be later used for extracting lexical chains
        self.n_sentences = len(sentences)

        self.build_graph(sentences)

    def extract_lexical_chains(self, n=None, out_file_path=None):
        self.lexical_chains = []
        if n is None:
            n = self.n_sentences
        elif self.n_sentences < n:
            n = self.n_sentences

        logging.info(f"Processing {n} chains")

        for index in range(0, n):
            index_str = str(index)

            nodes = [c for c in sorted(nx.strongly_connected_components(self.graphs[index_str]), key=len, reverse=True)]

            # adding only top-1
            self.lexical_chains.append(nodes[0])

        themes = {}
        for idx, item in enumerate(self.lexical_chains):
            items = list(item)
            themes[idx] = {'theme': ' '.join(items), 'score': len(items)}

        print(json.dumps(themes, indent=4))

        if out_file_path:
            save_to_json_file(themes, out_file_path)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # from vsg_utils.files import load_json_data
    # data_web_json = load_json_data('../../../../data/external/teslax.json')
    # content = data_web_json.get('content', '')

    """
    example from:
    
    Morris, J. and G. Hirst. Lexical cohesion computed by thesaural relations as an indicator of the
    structure of the text. In Computational Linguistics, 18(1):pp21-45. 1991.

    """
    content = (
        "In front of me lay a virgin crescent cut out of pine bush. A dozen houses were going up, in various stages "
        "of construction, surrounded by hummocks of dry earth and stands of precariously tall "
        "trees nude halfway up their trunks. They were the kind of trees you might see in the mountains. "
    )
    # A lexical chain spanning these three sentences is {virgin, pine, bush, trees, trunks, trees}

    lc = ThemeLexicalChains()
    lc.build_lexical_chains(content)
    lc.extract_lexical_chains(n=3)

    print(10 * "=")
    print("Graph: ")
    print(lc.graphs)

    print(10 * "=")
    print("Lexical Chain: ")
    print(lc.chains)

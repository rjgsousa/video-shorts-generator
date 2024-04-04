import json

from sklearn.feature_extraction.text import TfidfVectorizer


class Keywords:
    """
        A class for performing TF-IDF (Term Frequency-Inverse Document Frequency) analysis on a corpus of documents.

        TF-IDF is a classic technique in Natural Language Processing (NLP) that allows you to quantify the importance
        of a word in a document relative to the entire corpus. It provides a simple yet effective way to extract the
        most relevant words or features from text data.

        Despite being one of the oldest techniques in NLP, TF-IDF remains a popular and widely-used approach for
        various text mining and information retrieval tasks due to its simplicity and interpretability.
    """
    def __init__(self, threshold=0.15):
        self.threshold = threshold

    def _conduct_analysis(self, data):
        # documents = [sentence.strip() for sentence in data.split('.') if sentence.strip()]
        documents = [data]

        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(documents)

        feature_names = vectorizer.get_feature_names_out()

        # Create a dictionary to store the TF-IDF values for each term
        tfidf_dict = {}

        for i, document in enumerate(documents):
            feature_index = tfidf_matrix[i, :].nonzero()[1]
            tfidf_scores = zip(feature_index, [tfidf_matrix[i, x] for x in feature_index])

            # Store the TF-IDF values in the dictionary
            tfidf_dict[i] = {feature_names[i]: score for i, score in tfidf_scores}

        tfidf_dict = {k: v for k, v in tfidf_dict[0].items() if v > self.threshold}
        sorted_tfidf_dict = dict(sorted(tfidf_dict.items(), key=lambda item: item[1], reverse=True))

        return sorted_tfidf_dict

    def conduct_analysis_and_create_report(self, data: str, outfile):
        tfidf = self._conduct_analysis(data)
        print(10*"=")
        print("Presenting a report of the top key words available: ")
        print(tfidf)

        with open(outfile, "w") as file:
            json.dump(tfidf, file)

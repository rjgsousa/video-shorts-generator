import json
import logging
from typing import Union

from sklearn.feature_extraction.text import TfidfVectorizer
from vsg_utils.files import save_to_json_file


class ThemeKeywords:
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

    def conduct_analysis_and_create_report(self, data: str, out_file_path: Union[str | None] = None):
        tfidf = self._conduct_analysis(data)

        logging.info("Presenting a report of the top key words available: ")
        # final dictionary where we will record all themes
        result = {}
        for idx, item in enumerate(tfidf.items()):
            result[idx] = {'theme': item[0], 'score': item[1]}
        logging.info(json.dumps(result, indent=4))

        if out_file_path:
            save_to_json_file(result, out_file_path)

        return result


if __name__ == "__main__":
    from vsg_utils.files import load_json_data

    data_web_json = load_json_data('../../../../data/external/teslax.json')
    content = data_web_json.get('content', '')

    kd = ThemeKeywords()
    kd.conduct_analysis_and_create_report(data=content)

import numpy as np
from nltk.tokenize import sent_tokenize
from transformers import AutoTokenizer, AutoModel
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
import json

from vsg_utils.files import save_to_json_file

import torch
import torch.nn.functional as F


class ThemeTransformer:

    def __init__(self):
        # Download pre-trained tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-mpnet-base-v2")
        self.model = AutoModel.from_pretrained('sentence-transformers/all-mpnet-base-v2')

    @staticmethod
    def _mean_pooling(model_output, attention_mask):
        token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def conduct_analysis_and_create_report(self, data: str, num_themes=5, out_file_path=None):
        # Tokenize the document into sentences
        sentences = sent_tokenize(data)

        # Encode sentences and get sentence embeddings
        sentence_encoded = self.tokenizer(
            sentences,
            padding=True,
            truncation=True,
            return_tensors='pt'
        )

        # Compute token embeddings
        with torch.no_grad():
            model_output = self.model(**sentence_encoded)

        # Perform pooling
        sentence_embeddings = self._mean_pooling(model_output, sentence_encoded['attention_mask'])
        # Normalize embeddings
        sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)

        # Cluster sentence embeddings using K-means
        kmeans = KMeans(n_clusters=num_themes)
        kmeans.fit(sentence_embeddings)

        # Get the sentences closest to the centroid of each cluster
        closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_, sentence_embeddings)

        # Extract tokens from the closest sentences
        themes = {}
        for v, idx in enumerate(closest):
            tokens = self.tokenizer.convert_ids_to_tokens(sentence_encoded['input_ids'][idx], skip_special_tokens=True)
            themes[v] = ' '.join(tokens)

        # final dictionary where we will record all themes
        print(10*"=")
        result = {}
        for idx, item in enumerate(themes.items()):
            result[idx] = {'theme': item[1], 'score': np.NAN}

        print(json.dumps(result, indent=4))

        if out_file_path:
            save_to_json_file(themes, out_file_path)

        return themes


if __name__ == "__main__":
    from vsg_utils.files import load_json_data

    data_web_json = load_json_data('../../../../data/external/teslax.json')
    content = data_web_json.get('content', '')

    tf = ThemeTransformer()
    tf.conduct_analysis_and_create_report(data=content)

from gensim.models import FastText
from scipy.spatial.distance import cosine
from . import config


class WordModel:
    def __init__(self):
        self.model = FastText.load(config.WORD_MODEL)

    def is_in_vocab(self, word):
        return word in self.model.wv.vocab

    def get_vector(self, word):
        return self.model.wv[word]

    def get_word_similarity(self, word1, word2):
        try:
            return self.model.wv.similarity(word1, word2)
        except KeyError:
            return None
    
    def get_vector_similarity(self, vector1, vector2):
        return cosine(vector1, vector2)

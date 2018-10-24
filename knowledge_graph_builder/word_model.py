from gensim.models import FastText
from . import config

class WordModel:
    def __init__(self):
        self.model = FastText.load(config.WORD_MODEL)

    def is_in_vocab(self, word):
        return word in self.model.wv.vocab

    def get_vector(self, word):
        return self.model.wv[word]

    def get_similarity(self, word1, word2):
        return self.model.wv.similarity(word1, word2)

from .models import get_sessionmaker, Item, Property
from . import config

class KnowledgeGraph:
    def __init__(self):
        sessionmaker = get_sessionmaker()
        self.session = sessionmaker()

    

    

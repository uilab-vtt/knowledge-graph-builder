from sqlalchemy.orm.exc import NoResultFound
from .models import get_sessionmaker, Item, Property
from . import config

class KnowledgeGraph:
    def __init__(self):
        self.Sessionmaker = get_sessionmaker()
        self.session = self.Sessionmaker()

    def get_item_by_id_str(self, id_str):
        try:
            return self.session.query(Item).filter_by(id_str=id_str).one()
        except NoResultFound:
            return None

    def add_object_label(self, label):
        if 'id' in label:
            

    def add_behavior_label(self, label):
        pass

    def add_emotion_label(self, label):
        pass

    def add_relation_label(self, label):
        pass

    def add_location_label(self, label):
        pass

    def add_sound_label(self, label):
        pass

    def add_label(self, label):
        if label['type'] == 'object':
            self.add_object_label(label)
        elif label['type'] == 'behavior':
            self.add_behavior_label(label)
        elif label['type'] == 'emotion':
            self.add_emotion_label(label)
        elif label['type'] == 'relation':
            self.add_relation_label(label)
        elif label['type'] == 'location':
            self.add_location_label(label)
        elif label['type'] == 'sound':
            self.add_sound_label(label)

from sqlalchemy.orm.exc import NoResultFound
from .models import get_sessionmaker, Item, ValidTime, Box, Property
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

    # def get_item_by_coordinate(self, coordinate, seconds):
    #     try:
    #         ItemValidTime.query.filter(
    #             Patient.mother.has(phenoscore=10))


    # def add_object_label(self, label):
    #     if label['type'] == 'object':
    #         # Overwrite the entity
    #         entity = self.get_object_by_coord(label['seconds'], label['coordinates'])
    #         entity['entity_type'] = 'object'
    #         entity['class'] = label['class']
    #         entity['value'] = {'label': label['label']}

    #         if 'id' in label and label['id'] is not None:
    #             if 'input_ids' not in entity:
    #                 entity['input_ids'] = []
    #             entity['input_ids'].append(label['id'])
    #             self.ids[label['id']] = entity['id']

    #         coord_entity = self.get_coordinate_object(label['seconds'], label['coordinates'])
    #         prop_entity = self.get_property(label['seconds'], 'located_at', entity, coord_entity)

            
    #     if 'input_ids' not in entity:
    #                 entity['input_ids'] = []
    #             entity['input_ids'].append(label['id'])
    #             self.ids[label['id']] = entity['id']

    #         coord_entity = self.get_coordinate_object(label['seconds'], label['coordinates'])
    #         prop_entity = self.get_property(label['seconds'], 'located_at', entity, coord_entity)

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

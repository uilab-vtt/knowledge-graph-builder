from sqlalchemy import Column, ForeignKey, Boolean, Integer, String, Float, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.schema import UniqueConstraint

from . import config


Base = declarative_base()

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    id_str = Column(String(250), unique=True, nullable=True)
    classname = Column(String(250), default='', nullable=False)
    label = Column(Text, default='')
    value = Column(Text, default='')
    is_abstract = Column(Boolean, default=False)

    def as_dict(self):
        return {
            'type': 'item',
            'id': self.id,
            'id_str': self.id_str,
            'class': self.classname,
            'label': self.label,
            'value': self.value,
            'is_abstract': self.is_abstract,
        }

class ItemSimilarityRelation(Base):
    __tablename__ = 'item_similarity_relation'
    __table_args__ = (
        UniqueConstraint('item_id', 'another_item_id', name='_items_uc'),
    )
    id = Column(Integer, primary_key=True)
    similarity = Column(Float)
    item_id = Column(Integer, ForeignKey('item.id'))
    another_item_id = Column(Integer, ForeignKey('item.id'))
    item = relationship(Item, foreign_keys=[item_id])
    another_item = relationship(Item, foreign_keys=[another_item_id])

    def as_dict(self):
        return {
            'type': 'item_similarity_relation',
            'id': self.id,
            'similarity': self.similarity,
            'item_id': self.item_id,
            'another_item_id': self.another_item_id,
        }

class ValidTime(Base):
    __tablename__ = 'valid_time'
    id = Column(Integer, primary_key=True)
    time_start = Column(Float)
    time_end = Column(Float)
    item_id = Column(Integer, ForeignKey('item.id'))
    item = relationship(Item, foreign_keys=[item_id])

    def as_dict(self):
        return {
            'type': 'valid_time',
            'id': self.id,
            'time_start': self.time_start,
            'time_end': self.time_end,
            'item_id': self.item_id,
        }

class Box(Base):
    __tablename__ = 'box'
    id = Column(Integer, primary_key=True)
    time = Column(Float)
    x_start = Column(Integer)
    x_end = Column(Integer)
    y_start = Column(Integer)
    y_end = Column(Integer)
    item_id = Column(Integer, ForeignKey('item.id'))
    item = relationship(Item, foreign_keys=[item_id])

    def as_dict(self):
        return {
            'type': 'box',
            'id': self.id,
            'time': self.time,
            'x_start': self.x_start,
            'x_end': self.x_end,
            'y_start': self.y_start,
            'y_end': self.y_end,
            'item_id': self.item_id,
        }

class Property(Base):
    __tablename__ = 'property'
    id = Column(Integer, primary_key=True)
    id_str = Column(String(250), unique=True)
    classname = Column(String(250), nullable=False)
    value = Column(Text, default='')
    time_start = Column(Float)
    time_end = Column(Float)
    source_item_id = Column(Integer, ForeignKey('item.id'))
    target_item_id = Column(Integer, ForeignKey('item.id'))
    relation_item_id = Column(Integer, ForeignKey('item.id'))
    source = relationship(Item, foreign_keys=[source_item_id])
    target = relationship(Item, foreign_keys=[target_item_id])
    relation = relationship(Item, foreign_keys=[relation_item_id])

    def as_dict(self):
        return {
            'type': 'property',
            'id': self.id,
            'id_str': self.id_str,
            'classname': self.classname,
            'value': self.value,
            'time_start': self.time_start,
            'time_end': self.time_end,
            'source_item_id': self.source_item_id,
            'target_item_id': self.target_item_id,
            'relation_item_id': self.relation_item_id,
        }

def get_engine():
    return create_engine(config.SQLALCHEMY_ENGINE)

def init_db():
    Base.metadata.create_all(get_engine())

def get_sessionmaker():
    engine = get_engine()
    Base.metadata.bind = engine
    return sessionmaker(bind=engine)

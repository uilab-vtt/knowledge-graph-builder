from sqlalchemy import Column, ForeignKey, Boolean, Integer, String, Float, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

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

class ValidTime(Base):
    __tablename__ = 'valid_time'
    id = Column(Integer, primary_key=True)
    time_start = Column(Float)
    time_end = Column(Float)
    item_id = Column(Integer, ForeignKey('item.id'))
    item = relationship(Item, foreign_keys=[item_id])

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

def get_engine():
    return create_engine(config.SQLALCHEMY_ENGINE)

def init_db():
    Base.metadata.create_all(get_engine())

def get_sessionmaker():
    engine = get_engine()
    Base.metadata.bind = engine
    return sessionmaker(bind=engine)

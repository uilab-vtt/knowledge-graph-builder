from sqlalchemy import Column, ForeignKey, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from . import config

Base = declarative_base()

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    id_str = Column(String(250))
    classname = Column(String(250), nullable=False)
    value = Column(Text)
    time_start = Column(Float)
    time_end = Column(Float)
    x_start = Column(Integer)
    x_end = Column(Integer)
    y_start = Column(Integer)
    y_end = Column(Integer)

class Property(Base):
    __tablename__ = 'property'
    id = Column(Integer, primary_key=True)
    id_str = Column(String(250))
    classname = Column(String(250), nullable=False)
    value = Column(Text)
    time_start = Column(Float)
    time_end = Column(Float)
    source = relationship(Item)
    target = relationship(Item)

engine = create_engine(config.SQLALCHEMY_ENGINE)

def init_db():
    Base.metadata.create_all(engine)

def get_sessionmaker():
    Base.metadata.bind = engine
    return sessionmaker(bind=engine)



    

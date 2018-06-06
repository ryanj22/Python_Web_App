import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Parameter(Base):
    __tablename__ = 'Parameter'

    id = Column(Integer, primary_key=True)
    tagname = Column(String(250), nullable=False)
    blockname = Column(String(250))
    blocktype = Column(String(250))
    paramname = Column(String(250))
    paramvalue = Column(String(250))
    paramtype = Column(String(250))

engine = create_engine('sqlite:///partool.db')
Base.metadata.create_all(engine)

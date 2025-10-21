from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, select, update, delete, ForeignKey, Table
from sqlalchemy.orm import declarative_base, Session, relationship
from datetime import datetime
import random

engine = create_engine('sqlite:///relation.db', echo=True)
print(engine.connect())

Base = declarative_base()

experiment_subject = Table(
    'experiment_subject',
    Base.metadata,
    Column('experiment_id', Integer, ForeignKey('experiments.id'), primary_key=True),
    Column('subject_id', Integer, ForeignKey('subjects.id'), primary_key=True)
)

class Experiment(Base):
    __tablename__ = 'experiments'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    type = Column(Integer)
    finished = Column(Boolean, default=False)
    data_points = relationship("DataPoint", back_populates="experiment")
    subjects = relationship("Subject", secondary=experiment_subject, back_populates="experiments")

class DataPoint(Base):
    __tablename__ = 'data_points'
    id = Column(Integer, primary_key=True)
    real_value = Column(Float, nullable=False)
    target_value = Column(Float, nullable=False)
    experiment_id = Column(Integer, ForeignKey('experiments.id'))
    experiment = relationship("Experiment", back_populates="data_points")

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    gdpr_accepted = Column(Boolean, default=False)
    experiments = relationship("Experiment", secondary=experiment_subject, back_populates="subjects")    

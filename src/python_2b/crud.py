from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, select, update, delete
from sqlalchemy.orm import declarative_base, Session
from datetime import datetime
import random

engine = create_engine('sqlite:///test.db', echo=True)
print(engine.connect())

Base = declarative_base()

class Experiment(Base):
    __tablename__ = 'experiments'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    type = Column(Integer)
    finished = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Experiment(id={self.id}, title='{self.title}', type={self.type}, finished={self.finished})>"

class DataPoint(Base):
    __tablename__ = 'data_points'
    id = Column(Integer, primary_key=True)
    real_value = Column(Float, nullable=False)
    target_value = Column(Float, nullable=False)

    def __repr__(self):
        return f"<DataPoint(id={self.id}, real_value={self.real_value}, target_value={self.target_value})>"

Base.metadata.create_all(engine)

with Session(engine) as session:
    session.add_all(
       [Experiment(title=f"Experiment {i}", type=random.randint(1, 10)) for i in range(2)]
    )
    session.add_all(
        [DataPoint(real_value=random.uniform(0, 100), target_value=random.uniform(0, 100)) for _ in range(5)]
    )
    session.commit()

    experiments = session.scalars(select(Experiment)).all()
    data_points = session.scalars(select(DataPoint)).all()

    print(f"Experiments: {experiments}")
    print(f"Data Points: {data_points}")

    session.execute(update(Experiment).values(finished=True))
    session.commit()

    experiments = session.scalars(select(Experiment)).all()
    print(f"Experiments after update: {experiments}")

    session.execute(delete(Experiment))
    session.execute(delete(DataPoint))
    session.commit()
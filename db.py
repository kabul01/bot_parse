import os
import uuid

from dotenv import load_dotenv
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

engine = create_engine(
    f'postgresql+psycopg2://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/'
    f'{os.getenv("DB_NAME")}')



Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())


class TaskCodeForces(Base):
    __tablename__ = "task"

    uuid = Column(String, name="uuid", primary_key=True, default=generate_uuid)
    topic_task = Column(String(400), nullable=True)
    count_solution = Column(String(400), nullable=True)
    title = Column(String(400), nullable=True)
    number = Column(String, nullable=True)
    complexity = Column(String(400), nullable=True)
    url = Column(String(500), nullable=False)

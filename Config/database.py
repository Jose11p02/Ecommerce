import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

sqlite_file_name = '../database.sqlite'

base_dir = os.path.dirname(os.path.realpath(__file__))

database_url = f'sqlite:///{os.path.join(base_dir,sqlite_file_name)}'

engine = create_engine(database_url)

localSession = sessionmaker(autoflush=False,autocommit=False,bind=engine)

Base = declarative_base()

SECRETE_KEY = '7c22489a0742114a95c456d3e495639f4d96f192636f447ca59a7a93766d3e60'

TOKEN_SCONDS_EXP = 1
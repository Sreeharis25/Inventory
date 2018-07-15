"""Commands for aqlalchemy."""
from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


def create_db_engine():
    """For creating engine."""
    sm = create_engine(
        'mysql+mysqldb://weavedinadmin:admin@weavedin@localhost/weavedin')
    declarative_base().metadata.create_all(sm)
# DeclarativeBase.metadata.create_all(sm)
# Session = sessionmaker(bind=sm)
# session = Session()
# from inventory.models import *
# us=User(first_name='sree', last_name='s', access_token='hgfh', password='passw', email='s')
# session.add(us)
# session.commit()

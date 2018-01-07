from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
from sqlalchemy.orm import scoped_session, sessionmaker
import os

try:
    import config
    DB_URI = config.DB_URI
except Exception as e:
    DB_URI = os.environ['DB_URI']

# Replace 'sqlite:///rfg.db' with your path to database
engine = create_engine(DB_URI, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()
Base.metadata.create_all(engine)

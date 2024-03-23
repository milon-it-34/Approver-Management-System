# database.py
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from django.conf import settings

# Connection setup
DB_ENGINE = settings.DATABASES['default']['ENGINE'].rpartition('.')[-1]

if DB_ENGINE == 'postgresql_psycopg2':
    connection_string = ('postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}').format(**settings.DATABASES['default'])
    search_path = settings.DATABASES['default'].get('SCHEMA')
else:
    connection_string = ('{0}://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}').format(DB_ENGINE, **settings.DATABASES['default'])
    search_path = None

if DB_ENGINE == 'mysql':
    connection_string += '?charset=utf8'

engine = sa.create_engine(connection_string, pool_recycle=1800, pool_size=200, max_overflow=-1, pool_pre_ping=True)
if search_path:
    engine.execute("set search_path to {};".format(search_path))

# Session setup
Session = sessionmaker(bind=engine)

def create_session(secondary=False):
    if not secondary:
        return Session()
    else:
        # Define your secondary session setup if needed
        pass

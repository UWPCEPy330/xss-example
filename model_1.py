import os

from peewee import Model, CharField, IntegerField
from playhouse.db_url import connect

if os.path.exists('my_database.db'):
    os.remove('my_database.db')

db = connect(os.environ.get('DATABASE_URL', 'sqlite:///my_database.db'))


class Message(Model):
    content = CharField(max_length=1024, unique=True)

    class Meta:
        database = db

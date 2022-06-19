from datetime import datetime
from peewee import *


db = SqliteDatabase('base.db')


class BaseModel(Model):
    class Meta:
        database = db


class Liquids(BaseModel):
    name = TextField()
    salt = TextField()
    cost = IntegerField()
    count = IntegerField()


class News(BaseModel):
    title = TextField()
    text = TextField()


class Accounts(BaseModel):
    fio = TextField()
    email = TextField(unique=True)
    password = TextField()
    vk = BooleanField()
    history = TextField(null=True)
    registration_date = TimestampField(default=datetime.timestamp(datetime.now()))


class Messages(BaseModel):
    channel = IntegerField()
    whom = IntegerField()
    message = TextField()
    time = TimestampField(default=datetime.timestamp(datetime.now()))


class Queries(BaseModel):
    user_id = ForeignKeyField(Accounts, related_name='user')
    liquid_id = ForeignKeyField(Liquids, related_name='liquid')



def create_tables():
    with db:
        db.create_tables([Liquids, News, Accounts, Messages, Queries])

if __name__ == '__main__':
    create_tables()

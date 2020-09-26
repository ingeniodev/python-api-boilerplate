from peewee import *
from src.config import ConfigDatase

database = MySQLDatabase(ConfigDatase.Database, **{
    'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT',
    'use_unicode': True, 'host': ConfigDatase.Host,
    'port': ConfigDatase.Port, 'user': ConfigDatase.User,
    'password': ConfigDatase.Password})


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class Users(BaseModel):
    email = CharField()
    id_user = BigAutoField(column_name='idUser')
    name = CharField()
    password = CharField()

    class Meta:
        table_name = 'users'


class Tokens(BaseModel):
    date = DateTimeField(constraints=[SQL("DEFAULT current_timestamp()")])
    id_token = AutoField(column_name='idToken')
    id_user = ForeignKeyField(column_name='idUser',
                              field='id_user', model=Users)
    token = TextField()

    class Meta:
        table_name = 'tokens'

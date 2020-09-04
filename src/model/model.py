from peewee import *

database = MySQLDatabase('sensorium_users', **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT',
                                               'use_unicode': True, 'host': '192.168.0.20', 'port': 3308, 'user': 'root', 'password': 'inverifica'})


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

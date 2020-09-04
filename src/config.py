import os


class ConfigDatase:
    Host = os.getenv('DATABASE_HOST', 'localhost')
    Port = os.getenv('DATABASE_PORT', 3306)
    User = os.getenv('DATABASE_USER', 'admin')
    Password = os.getenv('DATABASE_PASSWORD', 'sercret')
    Database = os.getenv('DATABASE_BD', 'whoknows')


class ConfigDev:
    Debug = True


class ConfigProd:
    Debug = True

import os


class ConfigDatase:
    Host = os.getenv('DATABASE_HOST', 'localhost')
    Port = int(os.getenv('DATABASE_PORT', 3306))
    User = os.getenv('DATABASE_USER', 'admin')
    Password = os.getenv('DATABASE_PASSWORD', 'sercret')
    Database = os.getenv('DATABASE_BD', 'whoknows')


class ConfigDev:
    DEBUG = True
    TESTING = True


class ConfigProd:
    DEBUG = False
    TESTING = False


app_config = {
    'dev': ConfigDev,
    'prod': ConfigProd
}

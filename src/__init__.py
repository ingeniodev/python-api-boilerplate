import os
from flask import Flask, Blueprint
from flask_restplus import Api
from dotenv import load_dotenv

from .controller.user import api_user
from src.config import app_config

load_dotenv()
env_mode = os.getenv('FLASK_ENV', 'dev')

# creating flask api
api_v1 = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_v1, version='1.0', title='API',
          description='A boilerplate API',
          )

api.add_namespace(api_user)

app = Flask(__name__)
app.config.from_object(app_config[env_mode])
app.config['SWAGGER'] = {
    'title': 'Boilerplate API'
}

app.register_blueprint(api_v1)
app.run(debug=True)

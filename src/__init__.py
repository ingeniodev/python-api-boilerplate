from flask import Flask, Blueprint
from flask_restplus import Api
from .controller.user import api_user

api_v1 = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_v1, version='1.0', title='API',
          description='A boilerplate API',
          )

api.add_namespace(api_user)

app = Flask(__name__)
app.register_blueprint(api_v1)
app.run(debug=True)

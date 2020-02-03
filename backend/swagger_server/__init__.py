import connexion

from swagger_server import encoder
from swagger_server.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()
connex_app = connexion.App(__name__, specification_dir='./swagger/')
connex_app.app.json_encoder = encoder.JSONEncoder
connex_app.add_api('swagger.yaml', arguments={'title': 'Swagger Vacation calendar'}, validate_response=True)

# Get Flask application
app = connex_app.app
cors = CORS(app, resources={r"/vcalendar/*": {"origins": "http://localhost:\d*"}})
app.config.from_object(Config)
db.init_app(app)
app.app_context().push()

def create_app():
    connex_app.run(port=8080)

from swagger_server import orm
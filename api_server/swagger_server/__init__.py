import connexion

from swagger_server import encoder
from swagger_server.config import Config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
connex_app = connexion.App(__name__, specification_dir='./swagger/')
connex_app.app.json_encoder = encoder.JSONEncoder
connex_app.add_api('swagger.yaml', arguments={'title': 'Swagger Vacation calendar'})

# Get Flask application
app = connex_app.app
app.config.from_object(Config)
db.init_app(app)
app.app_context().push()

def create_app():
    connex_app.run(port=8080)

from swagger_server import orm
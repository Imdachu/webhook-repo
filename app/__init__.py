from flask import Flask
from .extensions import mongo
from .routes import main

def create_app():
    app = Flask(__name__)
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/webhookdb'  # Placeholder URI
    mongo.init_app(app)
    app.register_blueprint(main)
    return app 
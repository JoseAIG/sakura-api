from flask import Flask
from flask_cors import CORS
from database import db

from dotenv import load_dotenv
load_dotenv()

from config import *

from routes.auth import auth_bp

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
CORS(app)
db.init_app(app)

app.register_blueprint(auth_bp)

@app.route("/")
def index():
    return "Sakura manga viewer API"

if __name__ == '__main__':
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.run()
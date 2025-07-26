from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_migrate import Migrate
from dotenv import load_dotenv
load_dotenv()



app = Flask(__name__)
app.config.from_object('config.Config')  # Your config with DB URI and SECRET_KEY

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Setup Flask-Login manager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = "info"
login_manager.init_app(app)

# Import routes and API after app/db initialization
from routes import *
from api import *

# Run the app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create DB tables if not existing
    app.run(debug=True)

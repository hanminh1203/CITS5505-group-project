from flask import Flask, redirect, render_template, url_for
from database import db, ma
from flask_migrate import Migrate
# Import models here so Migrate can "see" them
from models import User, UserSkill, Skill, Request, Offer 
from flask_login import LoginManager
from api.routes import api_bp

app = Flask(__name__)

# Setup database and migrations
# TODO Move configuration into environment variables or a separate config file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ECHO"] = True
db.init_app(app)
ma.init_app(app)

# Set up Flask-Migrate
migrate = Migrate(app, db, render_as_batch=True)

# Set up Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
# This tells Flask-Login how to load a user from the ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register the API blueprint
app.register_blueprint(api_bp)

# API to serve the frontend
@app.route("/")
@app.route("/index.html")
def index():
    return render_template('index.html')

# TODO to generalize the methods below, we can use a single route with a parameter to determine which template to render. For example:
@app.route("/pages/<page>")
def fetchPage(page):
    return render_template(f'pages/{page}.page.html')

@app.route("/components/<component>")
def fetchComponent(component):
    return render_template(f'components/{component}.component.html')

@app.route("/modals/<modal>")
def fetchModal(modal):
    return render_template(f'modals/{modal}.modal.html')

@app.route("/<page>")
def subpage(page):
    return redirect(url_for('index', _anchor=page))

import traceback

from flask import Flask, current_app, redirect, render_template, request, url_for
from werkzeug.exceptions import HTTPException
from config import Config
from database import db, ma
from flask_migrate import Migrate
# Import models here so Migrate can "see" them
from models import User, UserSkill, Skill, Request, Offer 
from flask_login import LoginManager
from api.routes import api_bp

app = Flask(__name__)
app.config.from_object(Config)

# Setup database and migrations
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


# Global error handlers
@app.errorhandler(404)
def not_found(e):
    if request.path.startswith('/api/') or request.accept_mimetypes.accept_json:
        return handle_general_exception(e)
    
    return redirect(url_for('index', _anchor=404))

@app.errorhandler(Exception)
def handle_exception(e):
    return handle_general_exception(e)

def handle_general_exception(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    response = {
        "code": code,
        "message": str(e) if code != 500 else "An internal server error occurred."
    }
    if current_app.debug:
        response["stacktrace"] = traceback.format_exc()
    return response, code
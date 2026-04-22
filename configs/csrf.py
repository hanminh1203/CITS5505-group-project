from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
def init(app):
    csrf.init_app(app)
from flask_login import UserMixin
from sqlalchemy.orm import validates
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db
from app.models.mixins import AuditMixin, EntityMixin

class User(db.Model, UserMixin, EntityMixin, AuditMixin):
    __tablename__ = 'user'
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255))
    bio = db.Column(db.Text)
    address = db.Column(db.String(255))
    avatar = db.Column(db.String(255))

    # Relationships
    skills = db.relationship('UserSkill', backref='user', lazy=True)
    requests = db.relationship('Request', backref='owner', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @validates("email")
    def normalize_email(self, key, email):
        return email.strip().lower() if email else email
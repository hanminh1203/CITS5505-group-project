from database import db
from datetime import datetime
from enum import Enum
from sqlalchemy.sql import func
from flask_login import current_user
from sqlalchemy import event
from flask_login import UserMixin

# --- Reusable Enums ---

class SkillLevel(Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    EXPERT = "Expert"

class RequestStatus(Enum):
    OPEN = "Open"
    PENDING = "Pending"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class SessionFormat(Enum):
    ONLINE = "Online"
    OFFLINE = "Offline"
    HYBRID = "Hybrid"

# --- Mixin for Audit Columns ---
class AuditMixin:
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(
        db.DateTime, 
        server_default=func.now(), 
        onupdate=func.now()
    )
    created_by = db.Column(db.String(255))  # Typically stores a user ID
    updated_by = db.Column(db.String(255))
    version = db.Column(db.BigInteger, default=1)

# --- Models ---
class User(db.Model, UserMixin, AuditMixin):
    __tablename__ = 'user'
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255))
    bio = db.Column(db.Text)
    address = db.Column(db.String(255))
    avatar = db.Column(db.String(255))

    # Relationships
    skills = db.relationship('UserSkill', backref='user', lazy=True)
    requests = db.relationship('Request', backref='owner', lazy=True)
    
class UserSkill(db.Model):
    # Noted as a join table in the diagram, usually omits audit columns
    __tablename__ = 'user_skill'
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False)
    level = db.Column(db.Enum(SkillLevel), default=SkillLevel.BEGINNER)

    skill = db.relationship('Skill', lazy=True)

class SkillCategory(db.Model, AuditMixin):
    __tablename__ = 'skill_category'
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    skills = db.relationship('Skill', backref='category', lazy=True)

class Skill(db.Model, AuditMixin):
    __tablename__ = 'skill'
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('skill_category.id'))


class Request(db.Model, AuditMixin):
    __tablename__ = 'request'
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner_skill_id = db.Column(db.Integer, db.ForeignKey('user_skill.id'))
    status = db.Column(db.Enum(RequestStatus), default=RequestStatus.OPEN)
    format = db.Column(db.Enum(SessionFormat), default=SessionFormat.ONLINE)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    duration = db.Column(db.String(255))
    availability = db.Column(db.String(255))

    offers = db.relationship('Offer', backref='request', lazy=True)

class Offer(db.Model, AuditMixin):
    __tablename__ = 'offer'
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer, primary_key=True)
    offerer_id = db.Column(db.Integer, db.ForeignKey('user_skill.id'), nullable=False)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'), nullable=False)
    message = db.Column(db.Text)

    offerer = db.relationship('UserSkill', lazy=True)


# Add Audit event
def add_audit_data(mapper, connection, target):
    is_login = current_user and current_user.is_authenticated
    if not target.created_by:
        target.created_by = current_user.email if is_login else 'system'
    target.updated_by = current_user.email if is_login else 'system'
    target.version = target.version + 1 if target.id else 1


models_to_watch = [User, Skill, Request, Offer]
for model in models_to_watch:
    event.listen(model, 'before_insert', add_audit_data)
    event.listen(model, 'before_update', add_audit_data)

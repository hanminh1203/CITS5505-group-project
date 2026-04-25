from app.extensions import db
from app.models.enums import SkillLevel
from app.models.mixins import AuditMixin, EntityMixin

class SkillCategory(db.Model, EntityMixin, AuditMixin):
    __tablename__ = 'skill_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    skills = db.relationship('Skill', backref='category', lazy=True)

class Skill(db.Model, EntityMixin, AuditMixin):
    __tablename__ = 'skill'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('skill_category.id'))

class UserSkill(db.Model, EntityMixin):
    # Noted as a join table in the diagram, usually omits audit columns
    __tablename__ = 'user_skill'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'skill_id', name='uq_user_skill_user_id_skill_id'),
        {'sqlite_autoincrement': True},
    )
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False)
    level = db.Column(db.Enum(SkillLevel), default=SkillLevel.BEGINNER)

    skill = db.relationship('Skill', lazy=True)


from app.extensions import db
from app.models.enums import SkillLevel
from app.models.mixins import AuditMixin, EntityMixin


class Skill(db.Model, AuditMixin, EntityMixin):
    # Noted as a join table in the diagram, usually omits audit columns
    __tablename__ = 'skill'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    level = db.Column(db.Enum(SkillLevel), default=SkillLevel.BEGINNER)

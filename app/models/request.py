from app.extensions import db
from app.models.enums import RequestStatus, SessionFormat
from app.models.mixins import AuditMixin, EntityMixin
from app.models.skill import Skill


class Request(db.Model, EntityMixin, AuditMixin):
    __tablename__ = 'request'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner_skill_id = db.Column(
        db.Integer,
        db.ForeignKey('skill.id'),
        nullable=False,
    )
    skill_to_learn = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum(RequestStatus), default=RequestStatus.OPEN)
    format = db.Column(db.Enum(SessionFormat), nullable=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    duration = db.Column(db.String(255))
    availability = db.Column(db.String(255))
    selected_offer_id = db.Column(
        db.Integer,
        db.ForeignKey('offer.id'),
        nullable=True,
    )

    offers = db.relationship(
        'Offer',
        back_populates='request',
        foreign_keys='Offer.request_id',
        lazy=True,
    )
    owner_skill = db.relationship(Skill, lazy=True)
    selected_offer = db.relationship(
        'Offer',
        foreign_keys=[selected_offer_id],
        post_update=True,
        lazy=True,
    )


class Offer(db.Model, EntityMixin, AuditMixin):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    offer_skill_id = db.Column(
        db.Integer,
        db.ForeignKey('skill.id'),
        nullable=False,
    )
    request_id = db.Column(
        db.Integer,
        db.ForeignKey('request.id'),
        nullable=False,
    )
    message = db.Column(db.Text)

    request = db.relationship(
        Request,
        back_populates='offers',
        foreign_keys=[request_id],
        lazy=True,
    )
    offer_skill = db.relationship(Skill, lazy=True)

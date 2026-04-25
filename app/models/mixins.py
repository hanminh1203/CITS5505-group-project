from sqlalchemy.sql import func
from flask_login import current_user
from sqlalchemy import event

from app.extensions import db

class AuditMixin:
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(
        db.DateTime, 
        server_default=func.now(), 
        onupdate=func.now()
    )
    created_by = db.Column(db.String(255))
    updated_by = db.Column(db.String(255))
    
class EntityMixin:
    __table_args__ = {'sqlite_autoincrement': True}
    
    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.Integer, nullable=False, default=1)
    __mapper_args__ = {"version_id_col": version}
    
def add_audit_data(mapper, connection, target):
    is_login = current_user and current_user.is_authenticated
    if not target.created_by:
        target.created_by = current_user.email if is_login else 'system'
    target.updated_by = current_user.email if is_login else 'system'

def register_audit_hooks(*models):
    for model in models:
        event.listen(model, "before_insert", add_audit_data)
        event.listen(model, "before_update", add_audit_data)

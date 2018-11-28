from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import relationship

from app.database import db
from app.models.role import (
    role_association_table,
    RoleNames
)


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    roles = relationship("Role", secondary=role_association_table)
    calories_per_day = db.Column(db.Integer, nullable=True)

    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now)
    created_at = db.Column(db.TIMESTAMP, nullable=False, server_default=func.now())
    deleted_at = db.Column(db.TIMESTAMP, nullable=True)

    def delete(self):
        if self.deleted_at is None:
            self.deleted_at = datetime.now()

    def reactivate(self):
        self.deleted_at = None

    def save(self):
        db.session.add(self)
        db.session.commit()

    def is_user(self):
        return len(self.roles) == 0 or any(r.name == RoleNames.user for r in self.roles)

    def is_user_manager(self):
        return any(r.name == RoleNames.user_manager for r in self.roles)

    def is_admin(self):
        return any(r.name == RoleNames.admin for r in self.roles)

    @property
    def deleted(self):
        return self.deleted_at is not None

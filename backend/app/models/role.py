import enum

from sqlalchemy import func

from app.database import db


class RoleNames(enum.Enum):
    user = 0
    user_manager = 1
    admin = 2


class Role(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum(RoleNames))

    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now)
    created_at = db.Column(db.TIMESTAMP, nullable=False, server_default=func.now())
    deleted_at = db.Column(db.TIMESTAMP, nullable=True)


role_association_table = db.Table('user_role', db.metadata,
   db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
   db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
)
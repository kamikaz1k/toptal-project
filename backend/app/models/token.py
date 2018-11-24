from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey

from app.database import db


class Token(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", backref="user")
    jwt_token = db.Column(db.String(225), nullable=False, index=True, unique=True)

    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now)
    created_at = db.Column(db.TIMESTAMP, nullable=False, server_default=func.now())

    expires_on = db.Column(db.TIMESTAMP, nullable=False)
    revoked_on = db.Column(db.TIMESTAMP, nullable=True)

    @classmethod
    def find_by_token(cls, token):
        return cls.query.filter(
            cls.jwt_token == token,
            cls.revoked_on.is_(None),
            cls.expires_on > datetime.now()
        ).one_or_none()
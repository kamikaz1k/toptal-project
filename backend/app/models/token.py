from app.database import db
from app.models.user import User

from sqlalchemy import func
from sqlalchemy.schema import ForeignKey


class Token(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey(User.id), nullable=False)
    jwt_token = db.Column(db.String(225), nullable=False, index=True, unique=True)

    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now)
    created_at = db.Column(db.TIMESTAMP, nullable=False, server_default=func.now())

    expires_on = db.Column(db.TIMESTAMP, nullable=False)
    revoked_on = db.Column(db.TIMESTAMP, nullable=True)

from datetime import datetime

from sqlalchemy import func
from sqlalchemy.schema import ForeignKey

from app.database import db
from app.models.user import User


class Meal(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    owner_user_id = db.Column(db.Integer, ForeignKey(User.id), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    entry_datetime = db.Column(db.DateTime, nullable=False)
    calorie_count = db.Column(db.Integer, default=0)

    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now)
    created_at = db.Column(db.TIMESTAMP, nullable=False, server_default=func.now())
    deleted_at = db.Column(db.TIMESTAMP, nullable=True)

    @classmethod
    def get_by_id(cls, meal_id):
        return cls.query.filter(
            cls.id == meal_id,
            cls.deleted_at.is_(None)
        ).one_or_none()

    def delete(self):
        if self.deleted_at is None:
            self.deleted_at = datetime.now()

    def save(self):
        db.session.add(self)
        db.session.commit()

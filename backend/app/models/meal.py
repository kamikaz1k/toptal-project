from datetime import datetime
from dateutil.parser import parse

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

    entry_date = db.Column(db.Date, nullable=False)
    entry_time = db.Column(db.Time, nullable=False)

    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=func.now(), onupdate=func.now)
    created_at = db.Column(db.TIMESTAMP, nullable=False, server_default=func.now())
    deleted_at = db.Column(db.TIMESTAMP, nullable=True)

    @classmethod
    def create(
        cls,
        **props
    ):
        meal = cls()
        meal.update(**props)
        return meal

    def update(self, **props):
        self.owner_user_id = props.pop('owner_user_id', self.owner_user_id)
        self.text = props.pop('text', self.text)
        self.entry_datetime = parse(props.pop('entry_datetime', self.entry_datetime))
        self.calorie_count = props.pop('calorie_count', self.calorie_count)

        self.entry_date = self.entry_datetime.date()
        self.entry_time = self.entry_datetime.time()

        self.save()

    @classmethod
    def query_by_date_time_range(
        cls,
        owner_user_id,
        start_date=None,
        end_date=None,
        start_time=None,
        end_time=None
    ):

        query = cls.query.filter(cls.owner_user_id == owner_user_id)
        # .order_by() ?

        if start_date is not None and end_date is not None:
            query = query.filter(
                cls.entry_date.between(
                    start_date,
                    end_date
                )
            )

        if start_time is not None and end_time is not None:
            query = query.filter(
                cls.entry_time.between(
                    start_time,
                    end_time
                )
            )

        # pagination?
        return query.all()

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

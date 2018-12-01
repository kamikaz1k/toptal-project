from datetime import datetime
import bcrypt

from sqlalchemy import func
from sqlalchemy.orm import relationship

from app.database import db
from app.models.role import (
    role_association_table,
    RoleNames,
    Role
)


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    roles = relationship("Role", secondary=role_association_table)
    calories_per_day = db.Column(db.Integer, nullable=True)

    updated_at = db.Column(
        db.TIMESTAMP,
        nullable=False,
        default=func.now(),
        onupdate=func.now()
    )
    created_at = db.Column(
        db.TIMESTAMP,
        nullable=False,
        server_default=func.now()
    )
    deleted_at = db.Column(db.TIMESTAMP, nullable=True)

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password, bcrypt.gensalt())

    @classmethod
    def create(cls, **props):
        user = cls()
        user.password = cls.hash_password(props.pop('password'))
        user.update(**props)

        user_role = Role.get_user_role()
        user.roles.append(user_role)

        user.save()
        return user

    def update(self, **props):
        self.email = props.pop('email', self.email)
        self.name = props.pop('name', self.name)
        self.calories_per_day = props.pop(
            'calories_per_day',
            self.calories_per_day
        )

        is_admin = props.pop('is_admin', None)
        is_user_manager = props.pop('is_user_manager', None)

        if is_admin is not None:
            self.change_admin_role(is_admin)

        if is_user_manager is not None:
            self.change_user_manager_role(is_user_manager)

    def change_admin_role(self, is_admin):
        admin_role = Role.get_admin_role()
        if is_admin:
            self.roles.append(admin_role)
        else:
            if self.is_admin:
                self.roles.remove(admin_role)

    def change_user_manager_role(self, is_user_manager):
        user_manager_role = Role.get_user_manager_role()
        if is_user_manager:
            self.roles.append(user_manager_role)
        else:
            if self.is_user_manager:
                self.roles.remove(user_manager_role)

    @classmethod
    def find_by_credentials(cls, email, password):
        user = cls.query.filter(
            cls.email == email,
            cls.deleted_at.is_(None)
        ).one_or_none()

        if user and cls.verify_password(password, user.password):
            return user

    @staticmethod
    def verify_password(password, hashed_password):
        return bcrypt.checkpw(password, hashed_password)

    @classmethod
    def query_active_users(cls):
        return cls.query.filter(cls.deleted_at.is_(None))

    def delete(self):
        if self.deleted_at is None:
            self.deleted_at = datetime.now()

    def reactivate(self):
        self.deleted_at = None

    def save(self):
        db.session.add(self)
        db.session.commit()

    @property
    def is_user(self):
        return len(self.roles) == 0 or \
            any(r.name == RoleNames.user for r in self.roles)

    @property
    def is_user_manager(self):
        return any(r.name == RoleNames.user_manager for r in self.roles)

    @property
    def is_admin(self):
        return any(r.name == RoleNames.admin for r in self.roles)

    @property
    def can_update_users(self):
        return self.is_user_manager or self.is_admin

    @property
    def deleted(self):
        return self.deleted_at is not None

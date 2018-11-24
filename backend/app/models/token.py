from app.database import db


class Token(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    jwt_token = db.Column(db.String(225), nullable=False, index=True, unique=True)
    expires_on = db.Column(db.TIMESTAMP, nullable=False)

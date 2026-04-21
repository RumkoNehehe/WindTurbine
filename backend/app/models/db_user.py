from ..extensions import db


class AppUser(db.Model):
    __tablename__ = "app_user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # stores password hash
    user_type = db.Column(db.String(50), nullable=False)
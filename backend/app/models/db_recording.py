from ..extensions import db
from sqlalchemy.dialects.postgresql import JSONB

class Recording(db.Model):
    __tablename__ = "recording"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    data = db.Column(JSONB, nullable=False)
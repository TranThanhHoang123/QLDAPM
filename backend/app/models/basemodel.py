from app.extensions import db
from datetime import datetime


class BaseModel(db.Model):
    __abstract__ = True  # Để không tạo table riêng cho BaseModel

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

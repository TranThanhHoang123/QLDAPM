from app.extensions import db
from .basemodel import BaseModel

class Category(BaseModel):
    __tablename__ = "categories"

    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
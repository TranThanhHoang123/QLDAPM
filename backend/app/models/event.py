from app.extensions import db
from .basemodel import BaseModel
class Event(BaseModel):
    __tablename__ = "events"

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(200))
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    image = db.Column(db.Text,nullable=False)
    
    # Relationship
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id", ondelete="RESTRICT"),
        nullable=False
    )
    # Quan hệ ngược lại
    category = db.relationship("Category", back_populates="events")
    tickets = db.relationship("Ticket", back_populates="event")
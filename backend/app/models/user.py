from app.extensions import db
import enum
from .basemodel import BaseModel
class UserRole(enum.Enum):
    admin = "admin"
    manager = "manager"
    user = "user"

class User(BaseModel):
    __tablename__ = "users"

    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    name = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.user, nullable=False)

    # Quan hệ ngược
    tickets = db.relationship("Ticket", back_populates="user")
    cart = db.relationship("Cart", back_populates="user", uselist=False)
    orders = db.relationship("Order", back_populates="user")
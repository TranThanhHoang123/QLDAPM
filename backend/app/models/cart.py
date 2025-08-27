from app.extensions import db
from .basemodel import BaseModel
from app.models.ticket import TicketType


class Cart(BaseModel):
    __tablename__ = "carts"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,  # đảm bảo 1 user chỉ có 1 cart
    )

    # Quan hệ 1-1 với User
    user = db.relationship("User", back_populates="cart", uselist=False)

    # Quan hệ 1-n với CartItem
    items = db.relationship("CartItem", back_populates="cart")


class CartItem(BaseModel):
    __tablename__ = "cart_items"

    cart_id = db.Column(
        db.Integer, db.ForeignKey("carts.id", ondelete="CASCADE"), nullable=False
    )

    event_id = db.Column(
        db.Integer, db.ForeignKey("events.id", ondelete="CASCADE"), nullable=False
    )

    ticket_type = db.Column(
        db.Enum(TicketType, name="cart_ticket_type"), nullable=False
    )

    quantity = db.Column(db.Integer, nullable=False)

    # Quan hệ
    cart = db.relationship("Cart", back_populates="items")
    event = db.relationship("Event")

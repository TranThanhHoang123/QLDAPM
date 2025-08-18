from app.extensions import db
from datetime import datetime
from .basemodel import BaseModel
class Order(BaseModel):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    status = db.Column(
        db.String(20),
        default="PENDING"  # PENDING → PAID / FAILED / CANCELLED
    )
    payment_method = db.Column(db.String(20))  # momo / vnpay / cash
    total_amount = db.Column(db.Numeric(15, 2), default=0)
    # Quan hệ
    user = db.relationship("User", backref="orders")
    items = db.relationship("OrderItem", backref="order", cascade="all, delete-orphan")


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey("tickets.id"), nullable=False)
    price = db.Column(db.Float, nullable=False)

    # Quan hệ
    ticket = db.relationship("Ticket", backref="order_items")

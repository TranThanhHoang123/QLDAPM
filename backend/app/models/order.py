from app.extensions import db
from .basemodel import BaseModel
import enum
class OrderStatus(enum.Enum):
    PENDING = "PENDING" # Chờ thanh toán
    PAID = "PAID" # Đã thanh toán
    FAILED = "FAILED" # Thanh toán thất bại
    CANCELLED = "CANCELLED" # Hủy thanh toán / timeout

class PaymentMethod(enum.Enum):
    MOMO = "MOMO"
    VNPAY = "VNPAY"

class Order(BaseModel):
    __tablename__ = "orders"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False
    )

    status = db.Column(
        db.Enum(OrderStatus, name="order_status"),
        default=OrderStatus.PENDING,
        nullable=False
    )

    payment_method = db.Column(
        db.Enum(PaymentMethod, name="payment_method"),
        nullable=False
    )

    total_amount = db.Column(db.Numeric(15, 2), default=0)
    # Quan hệ
    user = db.relationship("User", back_populates="orders")
    items = db.relationship("OrderItem", back_populates="order")

class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(
        db.Integer,
        db.ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False
    )
    ticket_id = db.Column(
        db.Integer,
        db.ForeignKey("tickets.id", ondelete="RESTRICT"),
        nullable=False
    )
    price = db.Column(db.Float, nullable=False)

    # Quan hệ
    ticket = db.relationship("Ticket", back_populates="order_items")
    order = db.relationship("Order", back_populates="items")

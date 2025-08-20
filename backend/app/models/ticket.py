from app.extensions import db
from .basemodel import BaseModel
import enum

class TicketStatus(enum.Enum):
    AVAILABLE = "AVAILABLE"   # vé còn trống
    RESERVED = "RESERVED"     # vé đã được giữ chỗ (user đang thanh toán, chưa trả tiền nhưng tạm thời khóa vé lại).
    SOLD = "SOLD"             # vé đã thanh toán
    USED = "USED"             # vé đã check-in
    CANCELLED = "CANCELLED"   # vé đã hủy

class TicketType(enum.Enum):
    VIP = "VIP"
    STANDARD = "STANDARD"

class Ticket(BaseModel):
    __tablename__ = "tickets"

    event_id = db.Column(
        db.Integer,
        db.ForeignKey("events.id", ondelete="CASCADE"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=True
    )

    # Loại vé
    type = db.Column(
        db.Enum(TicketType, name="ticket_type"),
        nullable=False
    )

    # Giá vé
    price = db.Column(db.Numeric(10, 2), nullable=False)

    # Trạng thái vé
    status = db.Column(
        db.Enum(TicketStatus, name="ticket_status"),
        default=TicketStatus.AVAILABLE,
        nullable=False
    )

    # Relationship
    event = db.relationship("Event", back_populates="tickets")
    user = db.relationship("User", back_populates="tickets")
    order_items = db.relationship("OrderItem", back_populates="ticket")

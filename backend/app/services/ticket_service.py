from app.extensions import db
from app.models.ticket import Ticket, TicketType, TicketStatus
from sqlalchemy.exc import IntegrityError
class TicketService:
    def __init__(self):
        pass

    def get_tickets(self, **kwargs):
        query = Ticket.query

        # Lọc theo event_id
        if "event_id" in kwargs and kwargs["event_id"]:
            query = query.filter(Ticket.event_id == kwargs["event_id"])

        # Lọc theo user_id
        if "user_id" in kwargs and kwargs["user_id"]:
            query = query.filter(Ticket.user_id == kwargs["user_id"])

        # Lọc theo loại vé
        if "type" in kwargs and kwargs["type"]:
            try:
                ticket_type = TicketType(kwargs["type"])
                query = query.filter(Ticket.type == ticket_type)
            except ValueError:
                pass  # type không hợp lệ thì bỏ qua

        # Lọc theo trạng thái vé
        if "status" in kwargs and kwargs["status"]:
            try:
                ticket_status = TicketStatus(kwargs["status"])
                query = query.filter(Ticket.status == ticket_status)
            except ValueError:
                pass

        # Phân trang
        try:
            page = int(kwargs.get("page", 1))
        except ValueError:
            page = 1

        try:
            page_size = int(kwargs.get("page_size", 10))
        except ValueError:
            page_size = 10

        pagination = query.paginate(page=page, per_page=page_size, error_out=False)
        return pagination

    def get_tickets_by_user(self, user_id: int):
        return Ticket.query.filter_by(user_id=user_id).all()

    def get_ticket(self, ticket_id):
        return Ticket.query.get(ticket_id)
 
    def create_tickets(self, event_id: int, ticket_type: str, price: float, quantity: int):
        """
        Thêm nhiều vé vào một event.
        """
        try:
            ticket_type_enum = TicketType(ticket_type)
        except ValueError:
            raise ValueError("Invalid ticket type")

        tickets = []
        for _ in range(quantity):
            ticket = Ticket(
                event_id=event_id,
                type=ticket_type_enum,
                price=price,
                status=TicketStatus.AVAILABLE
            )
            tickets.append(ticket)

        db.session.bulk_save_objects(tickets)
        db.session.commit()
        return tickets

    def check_and_reserve_tickets(self, event_id, ticket_type, quantity, user_id):
        """
        Kiểm tra đủ vé AVAILABLE không, nếu có thì chuyển sang RESERVED
        """
        tickets = (
            Ticket.query
            .filter_by(event_id=event_id, type=ticket_type, status="AVAILABLE")
            .limit(quantity)
            .with_for_update() # lock rows
            .all()
        )

        if len(tickets) < quantity:
            return None, "Not enough tickets available"

        try:
            for t in tickets:
                t.status = TicketStatus.RESERVED
                t.user_id = user_id  # giữ chỗ cho user
            db.session.commit()
            return tickets, None
        except IntegrityError:
            db.session.rollback()
            return None, "Database error while reserving tickets"

    def confirm_tickets(self, ticket_ids):
        """
        Xác nhận thanh toán thành công -> RESERVED -> SOLD
        """
        tickets = Ticket.query.filter(
            Ticket.id.in_(ticket_ids),
            Ticket.status == TicketStatus.RESERVED
        ).all()

        for t in tickets:
            t.status = TicketStatus.SOLD

        db.session.commit()
        return tickets

    def release_tickets(self, ticket_ids):
        """
        Nếu thanh toán fail/timeout -> RESERVED -> AVAILABLE
        """
        tickets = Ticket.query.filter(
            Ticket.id.in_(ticket_ids),
            Ticket.status == TicketStatus.RESERVED
        ).all()

        for t in tickets:
            t.status = TicketStatus.AVAILABLE
            t.user_id = None

        db.session.commit()
        return tickets

    def mark_ticket_used(self, ticket_id: int):
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            raise ValueError("Ticket not found")
        if ticket.status != TicketStatus.PAID:
            raise ValueError("Ticket not valid for check-in")
        ticket.status = TicketStatus.USED
        db.session.commit()
        return ticket
    
    def cancel_ticket(self, ticket_id: int):
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            raise ValueError("Ticket not found")
        if ticket.status not in [TicketStatus.AVAILABLE, TicketStatus.BOOKED]:
            raise ValueError("Cannot cancel ticket already paid/used")
        ticket.status = TicketStatus.CANCELLED
        db.session.commit()
        return ticket

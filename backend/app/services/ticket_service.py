from app.extensions import db
from app.models.ticket import Ticket, TicketType, TicketStatus
from sqlalchemy.exc import IntegrityError
from app.models.event import Event
from datetime import datetime, timedelta, timezone
from sqlalchemy import func


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

        # Sắp xếp theo thời gian tạo mới nhất
        query = query.order_by(Ticket.created_at.desc())

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

    def get_tickets_by_user(self, user_id):
        return Ticket.query.filter_by(user_id=user_id).all()

    def get_ticket(self, ticket_id):
        return Ticket.query.get(ticket_id)

    def check_event_before_sale(self, event_id):
        """
        Kiểm tra event có còn đủ thời gian (>= 30 phút trước khi diễn ra)
        để cho phép thêm vé hay không.
        """
        vn_tz = timezone(timedelta(hours=7))
        now = datetime.now(vn_tz)

        event = Event.query.get(event_id)
        if not event:
            raise ValueError("Event not found")

        # Ép event_time về cùng timezone
        event_time = event.start_time
        if event_time.tzinfo is None:
            event_time = event_time.replace(tzinfo=vn_tz)

        if now > event_time - timedelta(minutes=30):
            raise ValueError(
                "Cannot add tickets. Event is starting in less than 30 minutes."
            )

        return True

    def create_tickets(self, event_id, ticket_type, price, quantity):
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
                status=TicketStatus.AVAILABLE,
            )
            tickets.append(ticket)

        db.session.bulk_save_objects(tickets)
        db.session.commit()
        return tickets

    def check_and_reserve_tickets(self, event_id, ticket_type, quantity, user_id):
        """
        Kiểm tra số lượng vé AVAILABLE và giữ chỗ (RESERVED) cho user
        """
        tickets = (
            Ticket.query.filter_by(
                event_id=event_id, type=ticket_type, status=TicketStatus.AVAILABLE
            )
            .limit(quantity)
            .with_for_update()  # lock để tránh race condition
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
        except IntegrityError as e:
            return None, f"Database error while reserving tickets: {str(e)}"

    def count_sold_by_month(self, year):
        """Số lượng vé bán (SOLD/USED) theo tháng"""
        data = (
            db.session.query(
                func.extract("month", Ticket.created_at).label("month"),
                func.count(Ticket.id).label("count"),
            )
            .filter(func.extract("year", Ticket.created_at) == year)
            .filter(Ticket.status.in_([TicketStatus.SOLD, TicketStatus.USED]))
            .group_by(func.extract("month", Ticket.created_at))
            .order_by("month")
            .all()
        )
        return [{"month": int(month), "count": count} for month, count in data]

    def count_sold_by_quarter(self, year):
        """Số lượng vé bán (SOLD/USED) theo quý"""
        data = (
            db.session.query(
                func.ceil(func.extract("month", Ticket.created_at) / 3).label(
                    "quarter"
                ),
                func.count(Ticket.id).label("count"),
            )
            .filter(func.extract("year", Ticket.created_at) == year)
            .filter(Ticket.status.in_([TicketStatus.SOLD, TicketStatus.USED]))
            .group_by("quarter")
            .order_by("quarter")
            .all()
        )
        return [{"quarter": int(q), "count": count} for q, count in data]

    def count_sold_by_year(self):
        """Số lượng vé bán (SOLD/USED) theo năm"""
        data = (
            db.session.query(
                func.extract("year", Ticket.created_at).label("year"),
                func.count(Ticket.id).label("count"),
            )
            .filter(Ticket.status.in_([TicketStatus.SOLD, TicketStatus.USED]))
            .group_by(func.extract("year", Ticket.created_at))
            .order_by("year")
            .all()
        )
        return [{"year": int(year), "count": count} for year, count in data]

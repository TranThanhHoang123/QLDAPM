from app.extensions import db
from app.models.order import Order, OrderItem, OrderStatus, PaymentMethod
from app.models.ticket import TicketStatus
from app.models.event import Event
from app.services.ticket_service import TicketService
from datetime import datetime, timedelta, timezone
from sqlalchemy import func
from flask import current_app


class OrderService:
    def __init__(self):
        self.ticket_service = TicketService()

    def get_orders(self, **kwargs):
        query = Order.query

        # Lọc theo user_id
        if "user_id" in kwargs and kwargs["user_id"]:
            query = query.filter(Order.user_id == kwargs["user_id"])

        if "status" in kwargs and kwargs["status"]:
            status = OrderStatus(kwargs["status"])
            query = query.filter(Order.status == status)

        if "payment_method" in kwargs and kwargs["payment_method"]:
            method = PaymentMethod(kwargs["payment_method"])
            query = query.filter(Order.payment_method == method)

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

    def get_order(self, order_id):
        return Order.query.get(order_id)

    def check_events_deadline(self, items):

        vn_tz = timezone(timedelta(hours=7))
        now = datetime.now(vn_tz)

        for item in items:
            event = Event.query.get(item["event_id"])
            if not event:
                return False, f"Event {item['event_id']} not found"

            event_time = event.start_time
            if event_time.tzinfo is None:
                event_time = event_time.replace(tzinfo=vn_tz)

            if now > event_time - timedelta(minutes=30):
                return (
                    False,
                    f"Cannot create order: Event '{event.title}' must be booked at least 30 minutes before start",
                )

        return True, None

    def create_order(self, user_id, payment_method, items):
        """
        items: list các vé muốn mua
        [
            {"event_id": 1, "ticket_type": "VIP", "quantity": 2},
            {"event_id": 1, "ticket_type": "NORMAL", "quantity": 3}
        ]
        """
        reserved_tickets = []

        for item in items:
            tickets, error = self.ticket_service.check_and_reserve_tickets(
                event_id=item["event_id"],
                ticket_type=item["ticket_type"],
                quantity=item["quantity"],
                user_id=user_id,
            )
            if error:
                return None, error

            reserved_tickets.extend(tickets)

        # 3. Tạo order
        order = Order(
            user_id=user_id,
            status=OrderStatus.PENDING,
            payment_method=PaymentMethod(payment_method),
            total_amount=0,  # sẽ cập nhật sau
        )
        db.session.add(order)
        db.session.flush()  # lấy order.id

        # 4. Tạo order_items & tính tổng tiền
        total_amount = 0
        for t in reserved_tickets:
            order_item = OrderItem(
                order_id=order.id,
                ticket_id=t.id,
                price=t.price,
            )
            total_amount += t.price
            db.session.add(order_item)

        # 5. Cập nhật tổng tiền
        order.total_amount = total_amount

        db.session.commit()
        return order, None

    def payment_success(self, order_id):
        current_app.logger.info(f"[payment_success] Bắt đầu xử lý order_id={order_id}")
        order = Order.query.get(order_id)

        if not order:
            current_app.logger.warning(
                f"[payment_success] Không tìm thấy order_id={order_id}"
            )
            return None, "Order not found"

        if order.status != OrderStatus.PENDING:
            current_app.logger.warning(
                f"[payment_success] Order {order_id} đã được xử lý trước đó. Trạng thái={order.status}"
            )
            return None, "Order already processed"

        try:
            order.status = OrderStatus.PAID
            current_app.logger.info(
                f"[payment_success] Order {order_id} đổi trạng thái -> PAID"
            )

            for item in order.items:
                ticket = item.ticket
                if ticket.status == TicketStatus.RESERVED:
                    ticket.status = TicketStatus.SOLD
                    current_app.logger.info(
                        f"[payment_success] Ticket {ticket.id} đổi trạng thái -> SOLD"
                    )

            db.session.commit()
            current_app.logger.info(
                f"[payment_success] Commit thành công cho order_id={order_id}"
            )
            return order, None
        except Exception as e:
            current_app.logger.error(
                f"[payment_success] Lỗi khi xử lý order_id={order_id}: {str(e)}"
            )
            return None, str(e)

    def payment_failed(self, order_id):
        current_app.logger.info(f"[payment_failed] Bắt đầu xử lý order_id={order_id}")
        order = Order.query.get(order_id)

        if not order:
            current_app.logger.warning(
                f"[payment_failed] Không tìm thấy order_id={order_id}"
            )
            return None, "Order not found"

        if order.status != OrderStatus.PENDING:
            current_app.logger.warning(
                f"[payment_failed] Order {order_id} đã được xử lý trước đó. Trạng thái={order.status}"
            )
            return None, "Order already processed"

        try:
            order.status = OrderStatus.CANCELLED
            current_app.logger.info(
                f"[payment_failed] Order {order_id} đổi trạng thái -> CANCELLED"
            )

            for item in order.items:
                ticket = item.ticket
                if ticket.status == TicketStatus.RESERVED:
                    ticket.status = TicketStatus.AVAILABLE
                    ticket.user_id = None
                    current_app.logger.info(
                        f"[payment_failed] Ticket {ticket.id} trả về trạng thái -> AVAILABLE"
                    )

            db.session.commit()
            current_app.logger.info(
                f"[payment_failed] Commit thành công cho order_id={order_id}"
            )
            return order, None
        except Exception as e:
            current_app.logger.error(
                f"[payment_failed] Lỗi khi xử lý order_id={order_id}: {str(e)}"
            )
            return None, str(e)

    def revenue_by_month(self, year):
        """Doanh thu + số đơn theo tháng trong 1 năm"""
        data = (
            db.session.query(
                func.extract("month", Order.created_at).label("month"),
                func.sum(Order.total_amount).label("revenue"),
                func.count(Order.id).label("orders"),
            )
            .filter(func.extract("year", Order.created_at) == year)
            .filter(Order.status == OrderStatus.PAID)
            .group_by(func.extract("month", Order.created_at))
            .order_by("month")
            .all()
        )
        return [
            {"month": int(month), "revenue": float(revenue or 0), "orders": orders}
            for month, revenue, orders in data
        ]

    def revenue_by_quarter(self, year):
        """Doanh thu + số đơn theo quý trong 1 năm"""
        data = (
            db.session.query(
                func.ceil(func.extract("month", Order.created_at) / 3).label("quarter"),
                func.sum(Order.total_amount).label("revenue"),
                func.count(Order.id).label("orders"),
            )
            .filter(func.extract("year", Order.created_at) == year)
            .filter(Order.status == OrderStatus.PAID)
            .group_by("quarter")
            .order_by("quarter")
            .all()
        )
        return [
            {"quarter": int(q), "revenue": float(revenue or 0), "orders": orders}
            for q, revenue, orders in data
        ]

    def revenue_by_year(self):
        """Doanh thu + số đơn theo năm"""
        data = (
            db.session.query(
                func.extract("year", Order.created_at).label("year"),
                func.sum(Order.total_amount).label("revenue"),
                func.count(Order.id).label("orders"),
            )
            .filter(Order.status == OrderStatus.PAID)
            .group_by(func.extract("year", Order.created_at))
            .order_by("year")
            .all()
        )
        return [
            {"year": int(year), "revenue": float(revenue or 0), "orders": orders}
            for year, revenue, orders in data
        ]

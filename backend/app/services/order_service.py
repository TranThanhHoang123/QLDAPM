from app.extensions import db
from app.models.order import Order, OrderItem
from app.models.ticket import TicketStatus
from app.services.ticket_service import TicketService
from sqlalchemy import func
class OrderService:
    def __init__(self):
         self.ticket_service = TicketService()

    def get_orders(self, **kwargs):
        query = Order.query

        # Lọc theo user_id
        if "user_id" in kwargs and kwargs["user_id"]:
            query = query.filter(Order.user_id == kwargs["user_id"])

        if "status" in kwargs and kwargs["status"]:
            query = query.filter(Order.status == kwargs["status"])
        
        if "payment_method" in kwargs and kwargs["payment_method"]:
            query = query.filter(Order.payment_method == kwargs["payment_method"])

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
                user_id=user_id
            )
            if error:
                db.session.rollback()
                return None, error

            reserved_tickets.extend(tickets)

        # 3. Tạo order
        order = Order(
            user_id=user_id,
            status="PENDING",
            payment_method=payment_method,
            total_amount=0  # sẽ cập nhật sau
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
        order = Order.query.get(order_id)
        if not order:
            return None, "Order not found"

        if order.status != "PENDING":
            return None, "Order already processed"

        try:
            # Cập nhật trạng thái order
            order.status = "PAID"
            # Lấy tất cả ticket từ order_items
            for item in order.items:  # quan hệ 1-n: Order.items
                ticket = item.ticket  # quan hệ n-1: OrderItem.ticket
                if ticket.status == TicketStatus.RESERVED:
                    ticket.status = TicketStatus.SOLD

            db.session.commit()
            return order, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    def payment_failed(self, order_id):
        order = Order.query.get(order_id)
        if not order:
            return None, "Order not found"

        if order.status != "PENDING":
            return None, "Order already processed"

        try:
            order.status = "CANCELLED"

            for item in order.items:
                ticket = item.ticket
                if ticket.status == TicketStatus.RESERVED:
                    ticket.status = TicketStatus.AVAILABLE
                    ticket.user_id = None

            db.session.commit()
            return order, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    def revenue_by_month(self, year: int):
        """Doanh thu + số đơn theo tháng trong 1 năm"""
        data = (
            db.session.query(
                func.extract("month", Order.created_at).label("month"),
                func.sum(Order.total_amount).label("revenue"),
                func.count(Order.id).label("orders"),
            )
            .filter(func.extract("year", Order.created_at) == year)
            .filter(Order.status == "PAID")
            .group_by(func.extract("month", Order.created_at))
            .order_by("month")
            .all()
        )
        return [
            {"month": int(month), "revenue": float(revenue or 0), "orders": orders}
            for month, revenue, orders in data
        ]

    def revenue_by_quarter(self, year: int):
        """Doanh thu + số đơn theo quý trong 1 năm"""
        data = (
            db.session.query(
                func.ceil(func.extract("month", Order.created_at) / 3).label("quarter"),
                func.sum(Order.total_amount).label("revenue"),
                func.count(Order.id).label("orders"),
            )
            .filter(func.extract("year", Order.created_at) == year)
            .filter(Order.status == "PAID")
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
            .filter(Order.status == "PAID")
            .group_by(func.extract("year", Order.created_at))
            .order_by("year")
            .all()
        )
        return [
            {"year": int(year), "revenue": float(revenue or 0), "orders": orders}
            for year, revenue, orders in data
        ]
     
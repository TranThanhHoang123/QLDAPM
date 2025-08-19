from apscheduler.schedulers.background import BackgroundScheduler
from app.extensions import db
from app.models.ticket import TicketStatus
from app.models.order import Order, OrderStatus
from datetime import datetime, timedelta

def release_expired_orders(app):
    with app.app_context():
        try:
            now = datetime.utcnow()
            # Tìm các order pending quá 15 phút
            expired_orders = Order.query.filter(
                Order.status == OrderStatus.PENDING,
                Order.updated_at < now - timedelta(minutes=15)
            ).all()

            # print(f"[{now}] Checking expired orders... Found {len(expired_orders)} orders")

            for order in expired_orders:
                # print(f"  -> Cancelling Order ID: {order.id}, User: {order.user_id}, "
                #       f"Total: {order.total_amount}, Updated At: {order.updated_at}")

                order.status = OrderStatus.CANCELLED

                # Giải phóng vé
                for item in order.items:
                    ticket = item.ticket
                    if ticket and ticket.status == TicketStatus.RESERVED:
                        # print(f"     - Releasing Ticket ID: {ticket.id} (was RESERVED)")
                        ticket.status = TicketStatus.AVAILABLE
                        ticket.user_id = None

            if expired_orders:
                db.session.commit()
                print(f"[{datetime.utcnow()}] Released {len(expired_orders)} expired orders")
            else:
                print(f"[{datetime.utcnow()}] No expired orders to release")

        except Exception as e:
            print("Error in release_expired_orders:", e)

def init_scheduler(app):
    scheduler = BackgroundScheduler()
    # Job giải phóng đơn hàng
    scheduler.add_job(
        func=lambda: release_expired_orders(app),
        trigger="interval",
        minutes=5,
        id="release_orders",
        replace_existing=True,
    )
    scheduler.start()
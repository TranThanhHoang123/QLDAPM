from apscheduler.schedulers.background import BackgroundScheduler
from app.extensions import db
from app.models.ticket import Ticket, TicketStatus
from datetime import datetime, timedelta

# Định nghĩa job
def release_expired_tickets(app):
    with app.app_context():
        try:
            now = datetime.utcnow()
            expired_tickets = Ticket.query.filter(
                Ticket.status == TicketStatus.RESERVED,
                Ticket.updated_at < now - timedelta(minutes=10)
            ).all()

            for ticket in expired_tickets:
                ticket.status = TicketStatus.AVAILABLE
                ticket.user_id = None

            if expired_tickets:
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("Error in release_expired_tickets:", e)


def init_scheduler(app):
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=lambda: release_expired_tickets(app),
        trigger="interval",
        minutes=5,
        id="release_tickets",
        replace_existing=True,
    )
    scheduler.start()
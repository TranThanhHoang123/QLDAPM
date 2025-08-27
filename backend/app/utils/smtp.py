import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime

# Load biến môi trường
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "taji3333333@gmail.com")
SMTP_PASS = os.getenv("SMTP_PASS", "nfdm nxqx bhzc lbvb ")

# Thư mục chứa template
TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__))


def render_template(template_name: str, context: dict) -> str:
    """Render file HTML template với data"""
    # env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template(template_name)
    return template.render(**context)


def send_email(to_email: str, subject: str, html_content: str):
    """Gửi email HTML qua SMTP"""
    msg = MIMEMultipart("alternative")
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    msg["Subject"] = subject

    # Gắn HTML
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, to_email, msg.as_string())
            print(f"Mail đã gửi tới {to_email}")
    except Exception as e:
        print(f"Lỗi gửi mail: {e}")


def send_payment_success_email(to_email: str, context: dict):
    """Hàm gửi email xác nhận thanh toán"""
    html_content = render_template("payment_success_smtp.html", context)
    subject = f"Xác nhận thanh toán đơn hàng #{context.get('order_id')}"
    send_email(to_email, subject, html_content)


def build_payment_success_context(order: dict) -> dict:
    """Convert order detail JSON -> context cho email template"""

    user = order["user"]
    items = []

    # Duyệt items
    for idx, item in enumerate(order["items"], start=1):
        ticket = item["ticket"]
        event = ticket["event"]
        items.append(
            {
                "index": idx,
                "event_title": event["title"],
                "event_start": event["start_time"],
                "event_end": event["end_time"],
                "event_location": event["location"],
                "ticket_type": ticket["type"],
                "price_vnd": f"{int(float(item['price'])):,} VND",
                "ticket_status": ticket["status"],
                "event_image": event["image"],
            }
        )

    # Build kết quả trả về
    context = {
        "order_id": order["id"],
        "status": order["status"],
        "customer_name": user["name"],
        "customer_email": user["email"],
        "payment_method": order["payment_method"],
        "total_amount_vnd": f"{int(float(order['total_amount'])):,} VND",
        "items": items,
        "ticket_status_overall": order["status"],
        "date": datetime.now().strftime("%d/%m/%Y"),
    }
    return context

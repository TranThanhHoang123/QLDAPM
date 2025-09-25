from app import create_app
from app.extensions import db
from app.models import User, Category, Ticket, Event
from app.models.ticket import TicketType
from datetime import datetime
from app.utils.jwt import JwtUtil

app = create_app()
jwt_util = JwtUtil()


# Khởi tạo dữ liệu user mẫu
def init_users():
    """Khởi tạo dữ liệu mẫu cho User"""
    if not User.query.first():  # Chỉ insert nếu DB trống
        password_hash = jwt_util.hash_password("admin")

        user1 = User(
            username="admin",
            email="admin@example.com",
            phone_number="0123456789",
            name="Administrator",
            password=password_hash,
            role="admin",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        user2 = User(
            username="customer",
            email="customer@example.com",
            phone_number="0987654321",
            name="Customer User",
            password=password_hash,
            role="user",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        user3 = User(
            username="manager",
            email="manager@example.com",
            phone_number="0112233445",
            name="Manager User",
            password=password_hash,
            role="manager",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        db.session.add_all([user1, user2, user3])
        db.session.commit()

        print("Sample users inserted!")
    else:
        print("Users already exist, skip inserting.")


# Khởi tạo dữ liệu category mẫu 1
def init_categories():
    """Khởi tạo dữ liệu mẫu cho Category"""
    if not Category.query.first():
        cat1 = Category(name="Hòa nhạc", description="Các sự kiện hòa nhạc âm nhạc")
        cat2 = Category(name="Hội thảo", description="Các sự kiện hội thảo, workshop")
        cat3 = Category(name="Thể thao", description="Các sự kiện thể thao, giải đấu")

        db.session.add_all([cat1, cat2, cat3])
        db.session.commit()

        print("Sample categories inserted!")
    else:
        print("Categories already exist, skip inserting.")


def init_events():
    """Khởi tạo dữ liệu mẫu cho Event + Ticket"""
    try:
        # ================== Event 1: Hội thảo ==================
        event1 = Event(
            title="Hội thảo Khoa học quốc gia",
            description="Buổi hội thảo chia sẻ về trí tuệ nhân tạo và ứng dụng trong đời sống.",
            location="Hội trường A, Đại học Bách Khoa",
            start_time=datetime(2025, 11, 15, 9, 0, 0),
            end_time=datetime(2025, 11, 15, 17, 0, 0),
            image="images/events/hoithao1.jpg",
            category_id=1,
        )

        # Ticket cho event1
        t1_vip = Ticket(event=event1, type=TicketType.VIP, price=30000)
        t1_std = Ticket(event=event1, type=TicketType.STANDARD, price=20000)

        event2 = Event(
            title="Hội thảo Công nghệ AI 2025",
            description="Buổi hội thảo chia sẻ về trí tuệ nhân tạo và ứng dụng trong đời sống.",
            location="Hội trường A, Đại học Bách Khoa",
            start_time=datetime(2025, 11, 15, 9, 0, 0),
            end_time=datetime(2025, 11, 15, 17, 0, 0),
            image="images/events/hoithao2.jpg",
            category_id=1,
        )

        # Ticket cho event1
        t2_vip = Ticket(event=event2, type=TicketType.VIP, price=30000)
        t2_std = Ticket(event=event2, type=TicketType.STANDARD, price=20000)

        event3 = Event(
            title="Hội thảo Công nghệ AI 2025",
            description="Buổi hội thảo chia sẻ về trí tuệ nhân tạo và ứng dụng trong đời sống.",
            location="Hội trường A, Đại học Bách Khoa",
            start_time=datetime(2025, 11, 15, 9, 0, 0),
            end_time=datetime(2025, 11, 15, 17, 0, 0),
            image="images/events/hoithao3.jpg",
            category_id=1,
        )

        # Ticket cho event1
        t3_vip = Ticket(event=event3, type=TicketType.VIP, price=30000)
        t3_std = Ticket(event=event3, type=TicketType.STANDARD, price=20000)

        event4 = Event(
            title="Hội thảo Công nghệ AI 2025",
            description="Buổi hội thảo chia sẻ về trí tuệ nhân tạo và ứng dụng trong đời sống.",
            location="Hội trường A, Đại học Bách Khoa",
            start_time=datetime(2025, 11, 15, 9, 0, 0),
            end_time=datetime(2025, 11, 15, 17, 0, 0),
            image="images/events/hoithao4.jpg",
            category_id=1,
        )

        # Ticket cho event1
        t4_vip = Ticket(event=event4, type=TicketType.VIP, price=30000)
        t4_std = Ticket(event=event4, type=TicketType.STANDARD, price=20000)

        event5 = Event(
            title="Hội thảo Công nghệ AI 2025",
            description="Buổi hội thảo chia sẻ về trí tuệ nhân tạo và ứng dụng trong đời sống.",
            location="Hội trường A, Đại học Bách Khoa",
            start_time=datetime(2025, 11, 15, 9, 0, 0),
            end_time=datetime(2025, 11, 15, 17, 0, 0),
            image="images/events/hoithao5.jpg",
            category_id=1,
        )

        # Ticket cho event1
        t5_vip = Ticket(event=event5, type=TicketType.VIP, price=30000)
        t5_std = Ticket(event=event5, type=TicketType.STANDARD, price=20000)

        event6 = Event(
            title="Hội thảo Công nghệ AI 2025",
            description="Buổi hội thảo chia sẻ về trí tuệ nhân tạo và ứng dụng trong đời sống.",
            location="Hội trường A, Đại học Bách Khoa",
            start_time=datetime(2025, 11, 15, 9, 0, 0),
            end_time=datetime(2025, 11, 15, 17, 0, 0),
            image="images/events/hoithao6.jpg",
            category_id=1,
        )

        # Ticket cho event1
        t6_vip = Ticket(event=event6, type=TicketType.VIP, price=30000)
        t6_std = Ticket(event=event6, type=TicketType.STANDARD, price=20000)

        event7 = Event(
            title="Hội thảo Công nghệ AI 2025",
            description="Buổi hội thảo chia sẻ về trí tuệ nhân tạo và ứng dụng trong đời sống.",
            location="Hội trường A, Đại học Bách Khoa",
            start_time=datetime(2025, 11, 15, 9, 0, 0),
            end_time=datetime(2025, 11, 15, 17, 0, 0),
            image="images/events/hoithao7.jpg",
            category_id=1,
        )

        # Ticket cho event1
        t7_vip = Ticket(event=event7, type=TicketType.VIP, price=30000)
        t7_std = Ticket(event=event7, type=TicketType.STANDARD, price=20000)

        event8 = Event(
            title="Hội thảo Công nghệ AI 2025",
            description="Buổi hội thảo chia sẻ về trí tuệ nhân tạo và ứng dụng trong đời sống.",
            location="Hội trường A, Đại học Bách Khoa",
            start_time=datetime(2025, 11, 15, 9, 0, 0),
            end_time=datetime(2025, 11, 15, 17, 0, 0),
            image="images/events/hoithao8.jpg",
            category_id=1,
        )

        # Ticket cho event1
        t8_vip = Ticket(event=event8, type=TicketType.VIP, price=30000)
        t8_std = Ticket(event=event8, type=TicketType.STANDARD, price=20000)

        # ================== Event 2: Hòa nhạc ==================
        event9 = Event(
            title="Hòa nhạc Giai điệu Mùa thu",
            description="Chương trình hòa nhạc với các bản nhạc cổ điển nổi tiếng.",
            location="Nhà hát Lớn Hà Nội",
            start_time=datetime(2025, 12, 1, 19, 0, 0),
            end_time=datetime(2025, 12, 1, 22, 0, 0),
            image="images/events/nhac1.jpg",
            category_id=2,
        )

        # Ticket cho event2
        t9_vip = Ticket(event=event9, type=TicketType.VIP, price=50000)
        t9_std = Ticket(event=event9, type=TicketType.STANDARD, price=30000)

        event10 = Event(
            title="Hòa nhạc Giai điệu Mùa thu",
            description="Chương trình hòa nhạc với các bản nhạc cổ điển nổi tiếng.",
            location="Nhà hát Lớn Hà Nội",
            start_time=datetime(2025, 12, 1, 19, 0, 0),
            end_time=datetime(2025, 12, 1, 22, 0, 0),
            image="images/events/nhac2.jpg",
            category_id=2,
        )

        # Ticket cho event2
        t10_vip = Ticket(event=event10, type=TicketType.VIP, price=50000)
        t10_std = Ticket(event=event10, type=TicketType.STANDARD, price=30000)

        event11 = Event(
            title="Hòa nhạc Giai điệu Mùa thu",
            description="Chương trình hòa nhạc với các bản nhạc cổ điển nổi tiếng.",
            location="Nhà hát Lớn Hà Nội",
            start_time=datetime(2025, 12, 1, 19, 0, 0),
            end_time=datetime(2025, 12, 1, 22, 0, 0),
            image="images/events/nhac3.jpg",
            category_id=2,
        )

        # Ticket cho event2
        t11_vip = Ticket(event=event11, type=TicketType.VIP, price=50000)
        t11_std = Ticket(event=event11, type=TicketType.STANDARD, price=30000)

        event12 = Event(
            title="Hòa nhạc Giai điệu Mùa thu",
            description="Chương trình hòa nhạc với các bản nhạc cổ điển nổi tiếng.",
            location="Nhà hát Lớn Hà Nội",
            start_time=datetime(2025, 12, 1, 19, 0, 0),
            end_time=datetime(2025, 12, 1, 22, 0, 0),
            image="images/events/nhac4.jpg",
            category_id=2,
        )

        # Ticket cho event2
        t12_vip = Ticket(event=event12, type=TicketType.VIP, price=50000)
        t12_std = Ticket(event=event12, type=TicketType.STANDARD, price=30000)

        event13 = Event(
            title="Hòa nhạc Giai điệu Mùa thu",
            description="Chương trình hòa nhạc với các bản nhạc cổ điển nổi tiếng.",
            location="Nhà hát Lớn Hà Nội",
            start_time=datetime(2025, 12, 1, 19, 0, 0),
            end_time=datetime(2025, 12, 1, 22, 0, 0),
            image="images/events/nhac5.jpg",
            category_id=2,
        )

        # Ticket cho event2
        t13_vip = Ticket(event=event13, type=TicketType.VIP, price=50000)
        t13_std = Ticket(event=event13, type=TicketType.STANDARD, price=30000)

        event14 = Event(
            title="Hòa nhạc Giai điệu Mùa thu",
            description="Chương trình hòa nhạc với các bản nhạc cổ điển nổi tiếng.",
            location="Nhà hát Lớn Hà Nội",
            start_time=datetime(2025, 12, 1, 19, 0, 0),
            end_time=datetime(2025, 12, 1, 22, 0, 0),
            image="images/events/nhac6.jpg",
            category_id=2,
        )

        # Ticket cho event2
        t14_vip = Ticket(event=event14, type=TicketType.VIP, price=50000)
        t14_std = Ticket(event=event14, type=TicketType.STANDARD, price=30000)

        event15 = Event(
            title="Hòa nhạc Giai điệu Mùa thu",
            description="Chương trình hòa nhạc với các bản nhạc cổ điển nổi tiếng.",
            location="Nhà hát Lớn Hà Nội",
            start_time=datetime(2025, 12, 1, 19, 0, 0),
            end_time=datetime(2025, 12, 1, 22, 0, 0),
            image="images/events/nhac7.jpg",
            category_id=2,
        )

        # Ticket cho event2
        t15_vip = Ticket(event=event15, type=TicketType.VIP, price=50000)
        t15_std = Ticket(event=event15, type=TicketType.STANDARD, price=30000)

        event16 = Event(
            title="Hòa nhạc Giai điệu Mùa thu",
            description="Chương trình hòa nhạc với các bản nhạc cổ điển nổi tiếng.",
            location="Nhà hát Lớn Hà Nội",
            start_time=datetime(2025, 12, 1, 19, 0, 0),
            end_time=datetime(2025, 12, 1, 22, 0, 0),
            image="images/events/nhac8.jpg",
            category_id=2,
        )

        # Ticket cho event2
        t16_vip = Ticket(event=event16, type=TicketType.VIP, price=50000)
        t16_std = Ticket(event=event16, type=TicketType.STANDARD, price=30000)

        # ================== Event 3: Thể thao ==================
        event17 = Event(
            title="Giải bóng đá Sinh viên 2025",
            description="Giải đấu bóng đá toàn quốc cho sinh viên.",
            location="Sân vận động Quốc gia Mỹ Đình",
            start_time=datetime(2025, 11, 20, 15, 0, 0),
            end_time=datetime(2025, 11, 20, 18, 0, 0),
            image="images/events/thethao1.jpg",
            category_id=3,
        )

        # Ticket cho event3
        t17_vip = Ticket(event=event17, type=TicketType.VIP, price=30000)
        t17_std = Ticket(event=event17, type=TicketType.STANDARD, price=10000)

        event18 = Event(
            title="Giải bóng đá Sinh viên 2025",
            description="Giải đấu bóng đá toàn quốc cho sinh viên.",
            location="Sân vận động Quốc gia Mỹ Đình",
            start_time=datetime(2025, 11, 20, 15, 0, 0),
            end_time=datetime(2025, 11, 20, 18, 0, 0),
            image="images/events/thethao2.jpg",
            category_id=3,
        )

        # Ticket cho event3
        t18_vip = Ticket(event=event18, type=TicketType.VIP, price=30000)
        t18_std = Ticket(event=event18, type=TicketType.STANDARD, price=10000)

        event19 = Event(
            title="Giải bóng đá Sinh viên 2025",
            description="Giải đấu bóng đá toàn quốc cho sinh viên.",
            location="Sân vận động Quốc gia Mỹ Đình",
            start_time=datetime(2025, 11, 20, 15, 0, 0),
            end_time=datetime(2025, 11, 20, 18, 0, 0),
            image="images/events/thethao3.jpg",
            category_id=3,
        )

        # Ticket cho event3
        t19_vip = Ticket(event=event19, type=TicketType.VIP, price=30000)
        t19_std = Ticket(event=event19, type=TicketType.STANDARD, price=10000)

        event20 = Event(
            title="Giải bóng đá Sinh viên 2025",
            description="Giải đấu bóng đá toàn quốc cho sinh viên.",
            location="Sân vận động Quốc gia Mỹ Đình",
            start_time=datetime(2025, 11, 20, 15, 0, 0),
            end_time=datetime(2025, 11, 20, 18, 0, 0),
            image="images/events/thethao4.jpg",
            category_id=3,
        )

        # Ticket cho event3
        t20_vip = Ticket(event=event20, type=TicketType.VIP, price=30000)
        t20_std = Ticket(event=event20, type=TicketType.STANDARD, price=10000)

        event21 = Event(
            title="Giải bóng đá Sinh viên 2025",
            description="Giải đấu bóng đá toàn quốc cho sinh viên.",
            location="Sân vận động Quốc gia Mỹ Đình",
            start_time=datetime(2025, 11, 20, 15, 0, 0),
            end_time=datetime(2025, 11, 20, 18, 0, 0),
            image="images/events/thethao5.jpg",
            category_id=3,
        )

        # Ticket cho event3
        t21_vip = Ticket(event=event21, type=TicketType.VIP, price=30000)
        t21_std = Ticket(event=event21, type=TicketType.STANDARD, price=10000)

        event22 = Event(
            title="Giải bóng đá Sinh viên 2025",
            description="Giải đấu bóng đá toàn quốc cho sinh viên.",
            location="Sân vận động Quốc gia Mỹ Đình",
            start_time=datetime(2025, 11, 20, 15, 0, 0),
            end_time=datetime(2025, 11, 20, 18, 0, 0),
            image="images/events/thethao6.jpg",
            category_id=3,
        )

        # Ticket cho event3
        t22_vip = Ticket(event=event22, type=TicketType.VIP, price=30000)
        t22_std = Ticket(event=event22, type=TicketType.STANDARD, price=10000)

        event23 = Event(
            title="Giải bóng đá Sinh viên 2025",
            description="Giải đấu bóng đá toàn quốc cho sinh viên.",
            location="Sân vận động Quốc gia Mỹ Đình",
            start_time=datetime(2025, 11, 20, 15, 0, 0),
            end_time=datetime(2025, 11, 20, 18, 0, 0),
            image="images/events/thethao7.jpg",
            category_id=3,
        )

        # Ticket cho event3
        t23_vip = Ticket(event=event23, type=TicketType.VIP, price=30000)
        t23_std = Ticket(event=event23, type=TicketType.STANDARD, price=10000)

        event24 = Event(
            title="Giải bóng đá Sinh viên 2025",
            description="Giải đấu bóng đá toàn quốc cho sinh viên.",
            location="Sân vận động Quốc gia Mỹ Đình",
            start_time=datetime(2025, 11, 20, 15, 0, 0),
            end_time=datetime(2025, 11, 20, 18, 0, 0),
            image="images/events/thethao8.jpg",
            category_id=3,
        )

        # Ticket cho event3
        t24_vip = Ticket(event=event24, type=TicketType.VIP, price=30000)
        t24_std = Ticket(event=event24, type=TicketType.STANDARD, price=10000)

        # Lưu vào DB
        db.session.add_all(
            [
                event1,
                event2,
                event3,
                event4,
                event5,
                event6,
                event7,
                event8,
                event9,
                event10,
                event11,
                event12,
                event13,
                event14,
                event15,
                event16,
                event17,
                event18,
                event19,
                event20,
                event21,
                event22,
                event23,
                event24,
                t1_vip,
                t2_vip,
                t3_vip,
                t4_vip,
                t5_vip,
                t6_vip,
                t7_vip,
                t8_vip,
                t9_vip,
                t10_vip,
                t11_vip,
                t12_vip,
                t13_vip,
                t14_vip,
                t15_vip,
                t16_vip,
                t17_vip,
                t18_vip,
                t19_vip,
                t20_vip,
                t21_vip,
                t22_vip,
                t23_vip,
                t24_vip,
                t1_std,
                t2_std,
                t3_std,
                t4_std,
                t5_std,
                t6_std,
                t7_std,
                t8_std,
                t9_std,
                t10_std,
                t11_std,
                t12_std,
                t13_std,
                t14_std,
                t15_std,
                t16_std,
                t17_std,
                t18_std,
                t19_std,
                t20_std,
                t21_std,
                t22_std,
                t23_std,
                t24_std,
            ]
        )
        db.session.commit()

        print("Sample events + tickets inserted!")

    except Exception as e:
        print(f"Events already exist or error occurred: {e}")


with app.app_context():
    db.create_all()
    init_users()
    init_categories()
    init_events()
    print("Database created successfully!")

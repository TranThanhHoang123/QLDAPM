from app import create_app
from app.extensions import db
from app.models import User, Category
from datetime import datetime
from app.utils.jwt import JwtUtil
app = create_app()
jwt_util = JwtUtil()

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
            updated_at=datetime.utcnow()
        )

        user2 = User(
            username="customer",
            email="customer@example.com",
            phone_number="0987654321",
            name="Customer User",
            password=password_hash,
            role="user",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        user3 = User(
            username="manager",
            email="manager@example.com",
            phone_number="0112233445",
            name="Manager User",
            password=password_hash,
            role="manager",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        db.session.add_all([user1, user2, user3])
        db.session.commit()

        print("✅ Sample users inserted!")
    else:
        print("⚠️ Users already exist, skip inserting.")


def init_categories():
    """Khởi tạo dữ liệu mẫu cho Category"""
    if not Category.query.first():
        cat1 = Category(name="Hòa nhạc", description="Các sự kiện hòa nhạc âm nhạc")
        cat2 = Category(name="Hội thảo", description="Các sự kiện hội thảo, workshop")
        cat3 = Category(name="Thể thao", description="Các sự kiện thể thao, giải đấu")

        db.session.add_all([cat1, cat2, cat3])
        db.session.commit()

        print("✅ Sample categories inserted!")
    else:
        print("⚠️ Categories already exist, skip inserting.")


with app.app_context():
    db.create_all()
    init_users()
    init_categories()
    print("✅ Database created successfully!")
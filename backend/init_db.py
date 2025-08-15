from app import create_app
from app.extensions import db
from app.models import User
from datetime import datetime
from app.utils.jwt import JwtUtil
app = create_app()
jwt_util = JwtUtil()
with app.app_context():
    db.create_all()
     # Insert dữ liệu mẫu
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

        print("✅ Database created & sample data inserted!")
    else:
        print("⚠️ Database already has data, skip inserting.")

    print("✅ Database created successfully!")

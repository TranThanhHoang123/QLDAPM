from app import create_app
from app.extensions import db
from app.models import User
app = create_app()

with app.app_context():
    db.create_all()
     # Insert dữ liệu mẫu
    if not User.query.first():  # Chỉ insert nếu DB trống
        user1 = User(username="Admin", email="admin@example.com")
        user2 = User(username="Test User", email="test@example.com")

        db.session.add_all([user1, user2])
        db.session.commit()

        print("✅ Database created & sample data inserted!")
    else:
        print("⚠️ Database already has data, skip inserting.")

    print("✅ Database created successfully!")

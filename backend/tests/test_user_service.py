import unittest
from datetime import datetime
from app import create_app
from app.extensions import db
from app.models import User
from app.services.user_service import UserService
from app.utils.jwt import JwtUtil

class UserServiceTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Tạo app test
        cls.app = create_app("app.config.TestingConfig")
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()
        cls.jwt_util = JwtUtil()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        # Xóa dữ liệu trước mỗi test
        db.session.query(User).delete()
        db.session.commit()
        self.service = UserService()

    def test_login_success(self):
        # tạo user thật trong DB test
        password_hash = self.jwt_util.hash_password("123456")
        user = User(
            username="realuser",
            email="real@example.com",
            phone_number="0123456789",
            name="Administrator",
            password=password_hash,
            role="admin",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(user)
        db.session.commit()

        result, error = self.service.login("realuser", "123456")

        self.assertIsNone(error)
        self.assertEqual(result["user"]["username"], "realuser")
        self.assertIn("token", result)

    def test_login_failure(self):
        # đăng nhập giả
        result, error = self.service.login("nonexist", "any_password")

        self.assertIsNone(result)
        self.assertEqual(error, "User not found")

if __name__ == "__main__":
    unittest.main()

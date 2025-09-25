from app.extensions import db
from sqlalchemy import func
from app.models.user import User, UserRole
from datetime import datetime, timedelta
from app.utils.jwt import JwtUtil
from sqlalchemy.exc import IntegrityError


class UserService:
    def __init__(self):
        self.jwt_util = JwtUtil()

    def get_users(self, **kwargs):
        query = User.query

        # Lọc
        if "username" in kwargs and kwargs["username"]:
            query = query.filter(User.username.ilike(f"%{kwargs['username']}%"))

        if "email" in kwargs and kwargs["email"]:
            query = query.filter(User.email == kwargs["email"])

        # Sắp xếp theo thời gian tạo mới nhất
        query = query.order_by(User.created_at.desc())

        try:
            page = int(kwargs.get("page", 1))
        except ValueError:
            page = 1

        try:
            page_size = int(kwargs.get("page_size", 10))
        except ValueError:
            page_size = 10

        # Phân trang
        pagination = query.paginate(page=page, per_page=page_size, error_out=False)
        return pagination

    def create_user(self, **data):
        # Hash password
        data["password"] = self.jwt_util.hash_password(data["password"])
        data["role"] = UserRole.manager
        user = User(**data)
        db.session.add(user)
        try:
            db.session.commit()
            return user
        except IntegrityError as e:
            # Lấy thông tin chi tiết từ lỗi
            msg = str(e.orig).lower()

            if "username" in msg:
                raise ValueError("Username already exists")
            elif "email" in msg:
                raise ValueError("Email already exists")

    def register(self, **data):
        # Hash password nếu có
        data["password"] = self.jwt_util.hash_password(data["password"])

        # Role mặc định cho người đăng ký
        data["role"] = UserRole.user

        user = User(**data)
        db.session.add(user)
        try:
            db.session.commit()
            return user
        except IntegrityError as e:
            # Lấy thông tin chi tiết từ lỗi
            msg = str(e.orig).lower()

            if "username" in msg:
                raise ValueError("Username already exists")
            elif "email" in msg:
                raise ValueError("Email already exists")

    def update_user(self, user_id, **data):
        user = User.query.get(user_id)
        if not user:
            return None

        for field, value in data.items():
            if hasattr(user, field) and value is not None:
                setattr(user, field, value)

        db.session.commit()
        return user

    def delete_user(self, user_id):
        user = User.query.filter(
            User.id == user_id, User.role != "admin"  # Chỉ lấy user không phải admin
        ).first()

        if not user:
            return False

        db.session.delete(user)
        db.session.commit()
        return True

    def login(self, username, password):
        # 1. Tìm user theo username
        user = User.query.filter_by(username=username).first()
        if not user:
            return None, "User not found"

        # 2. Kiểm tra mật khẩu
        if not self.jwt_util.check_password(password, user.password):
            return None, "Invalid password"

        # 3. Tạo token
        token = self.jwt_util.parse_id_to_token(user.id)
        expired_at = datetime.utcnow() + timedelta(
            minutes=self.jwt_util.token_expire_minutes
        )

        return {
            "token": token,
            "expired_at": expired_at.isoformat() + "Z",  # Trả ISO format UTC
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role.value if user.role else None,
            },
        }, None

    def change_password(self, user_id, old_password, new_password):
        # 1. Tìm user theo ID
        user = User.query.get(user_id)
        if not user:
            return None, "User not found"

        # 2. Kiểm tra mật khẩu cũ
        if not self.jwt_util.check_password(old_password, user.password):
            return None, "Old password is incorrect"

        # 3. Hash mật khẩu mới và lưu
        hashed_new_password = self.jwt_util.hash_password(new_password)
        user.password = hashed_new_password
        user.updated_at = datetime.utcnow()

        # 4. Commit DB
        db.session.commit()

        return {"message": "Password changed successfully"}, None

    def count_by_month(self, year):
        """Số lượng khách hàng (role=user) đăng ký theo tháng"""
        data = (
            db.session.query(
                func.extract("month", User.created_at).label("month"),
                func.count(User.id).label("count"),
            )
            .filter(func.extract("year", User.created_at) == year)
            .filter(User.role == UserRole.user)  # chỉ lấy khách hàng
            .group_by(func.extract("month", User.created_at))
            .order_by("month")
            .all()
        )
        return [{"month": int(month), "count": count} for month, count in data]

    def count_by_quarter(self, year):
        """Số lượng khách hàng (role=user) đăng ký theo quý"""
        data = (
            db.session.query(
                func.ceil(func.extract("month", User.created_at) / 3).label("quarter"),
                func.count(User.id).label("count"),
            )
            .filter(func.extract("year", User.created_at) == year)
            .filter(User.role == UserRole.user)  # lọc khách hàng
            .group_by("quarter")
            .order_by("quarter")
            .all()
        )
        return [{"quarter": int(q), "count": count} for q, count in data]

    def count_by_year(self):
        """Số lượng khách hàng (role=user) đăng ký theo năm"""
        data = (
            db.session.query(
                func.extract("year", User.created_at).label("year"),
                func.count(User.id).label("count"),
            )
            .filter(User.role == UserRole.user)  # lọc khách hàng
            .group_by(func.extract("year", User.created_at))
            .order_by("year")
            .all()
        )
        return [{"year": int(year), "count": count} for year, count in data]

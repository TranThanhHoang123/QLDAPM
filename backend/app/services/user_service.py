from app.extensions import db
from app.models.user import User, UserRole
from datetime import datetime, timedelta
from app.utils.jwt import JwtUtil
class UserService:
    def __init__(self):
        self.jwt_util = JwtUtil()

    def get_users(self, **kwargs):
        query = User.query

        # Lọc đặc biệt
        if "username" in kwargs and kwargs["username"]:
            query = query.filter(User.username.ilike(f"%{kwargs['username']}%"))

        if "email" in kwargs and kwargs["email"]:
            query = query.filter(User.email == kwargs["email"])

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
        # Hash password nếu có
        if "password" in data and data["password"]:
            data["password"] = self.jwt_util.hash_password(data["password"])
        data["role"] = UserRole.manager
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return user
    
    def register(self, **data):
        # Hash password nếu có
        if "password" in data and data["password"]:
            data["password"] = self.jwt_util.hash_password(data["password"])

        # Role mặc định cho người đăng ký
        data["role"] = UserRole.user

        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return user

    def update_user(self, user_id, **data):
        user = User.query.get(user_id)
        if not user:
            return None

        # Không cho update mấy field này
        disallowed = {"id", "created_at", "updated_at", "password"}
        for field, value in data.items():
            if field not in disallowed and hasattr(user, field) and value is not None:
                setattr(user, field, value)

        db.session.commit()
        return user

    def delete_user(self, user_id):
        user = User.query.filter(
            User.id == user_id,
            User.role != "admin"  # Chỉ lấy user không phải admin
        ).first()
        
        if not user:
            return False
        
        db.session.delete(user)
        db.session.commit()
        return True

    def login(self, username: str, password: str):
        # 1. Tìm user theo username
        user = User.query.filter_by(username=username).first()
        if not user:
            return None, "User not found"

        # 2. Kiểm tra mật khẩu
        if not self.jwt_util.check_password(password, user.password):
            return None, "Invalid password"

        # 3. Tạo token
        token = self.jwt_util.parse_id_to_token(user.id)
        expired_at = datetime.utcnow() + timedelta(minutes=self.jwt_util.token_expire_minutes)

        return {
            "token": token,
            "expired_at": expired_at.isoformat() + "Z",  # Trả ISO format UTC
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role.value if user.role else None
            }
        }, None
    
    def change_password(self, user_id: int, old_password: str, new_password: str):
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
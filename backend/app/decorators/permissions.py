from functools import wraps
from flask import request, jsonify, g
from app.models.user import User
from app.utils.jwt import JwtUtil

jwt_util = JwtUtil()

# Thứ tự quyền từ thấp đến cao
ROLE_HIERARCHY = {
    "user": 1,
    "manager": 2,
    "admin": 3
}

def my_permission(required_roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Lấy token từ header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({"message": "Missing or invalid token"}), 401
            
            token = auth_header.split(" ")[1]

            try:
                # Giải mã token → lấy user
                user_id = jwt_util.parse_token_to_id(token)
                user = User.query.get(user_id)
                if not user:
                    return jsonify({"message": "User not found"}), 404

                # Lưu user vào g để controller dùng
                g.current_user = user

                # Lấy role hiện tại của user (Enum hoặc string)
                user_role = user.role.value if hasattr(user.role, "value") else user.role

                # Lấy bậc role cao nhất mà API yêu cầu
                min_required_level = max(ROLE_HIERARCHY[r] for r in required_roles)
                user_level = ROLE_HIERARCHY.get(user_role, 0)

                if user_level < min_required_level:
                    return jsonify({"message": "Permission denied"}), 403

                return f(*args, **kwargs)

            except Exception as e:
                return jsonify({"message": str(e)}), 401

        return wrapper
    return decorator

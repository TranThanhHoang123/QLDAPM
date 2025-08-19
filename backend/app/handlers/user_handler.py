from flask import Blueprint, request, jsonify, g
from app.services.user_service import UserService
from app.decorators.permissions import my_permission
from app.schemas.user import (
    UserListSchema,
    UserDetailSchema,
    UserCreateSchema,
    UserUpdateSchema,
    UserChangePasswordSchema
)

bp = Blueprint("users", __name__, url_prefix="/user")
user_service = UserService()

user_list_schema = UserListSchema(many=True)
user_detail_schema = UserDetailSchema()
user_create_schema = UserCreateSchema()
user_update_schema = UserUpdateSchema()
user_change_password_schema = UserChangePasswordSchema()

@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    result, error = user_service.login(username=username, password=password)
    if error:
        return jsonify({"message": error}), 401

    return jsonify(result), 200

@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    errors = user_create_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    try:
        user = user_service.register(**data)
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    return user_detail_schema.dump(user), 201

@bp.route("/", methods=["GET"])
@my_permission("manager")
def get_users():
    params = request.args.to_dict()
    pagination = user_service.get_users(**params)

    return jsonify({
        "items": user_list_schema.dump(pagination.items),
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages
    })

@bp.route("/", methods=["POST"])
@my_permission("admin")
def create_user():
    data = request.get_json()
    errors = user_create_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    try:
        user = user_service.create_user(**data)
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    return user_detail_schema.dump(user), 201

@bp.route("/me", methods=["PUT"])
@my_permission("user")
def update_user():
    data = request.get_json()
    errors = user_update_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400

    # Lấy user từ token
    current_user = g.current_user

    user = user_service.update_user(user_id=current_user.id, **data)
    if not user:
        return jsonify({"message": "User not found"}), 404

    return user_detail_schema.dump(user), 200

@bp.route("/me", methods=["GET"])
@my_permission("user")
def get_profile():
    user = g.current_user
    return user_detail_schema.dump(user), 200

@bp.route("/me/change-password", methods=["PUT"])
@my_permission("user")
def change_password():
    # Validate request body
    data = request.get_json()
    errors = user_change_password_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    old_password = data["old_password"]
    new_password = data["new_password"]

    result, error = user_service.change_password(
        user_id=g.current_user.id,
        old_password=old_password,
        new_password=new_password
    )

    if error:
        return jsonify({"message": error}), 400

    return jsonify(result), 200

@bp.route("/<int:user_id>", methods=["DELETE"])
@my_permission("admin")
def delete_user(user_id):
    success = user_service.delete_user(user_id)
    if not success:
        return jsonify({"message": "User not found"}), 404
    return jsonify({"message": "User deleted successfully"})

@bp.route("/stats/monthly/<int:year>")
@my_permission("manager")
def stats_user_monthly(year):
    return jsonify(user_service.count_by_month(year))

@bp.route("/stats/quarterly/<int:year>")
@my_permission("manager")
def stats_user_quarterly(year):
    return jsonify(user_service.count_by_quarter(year))

@bp.route("/stats/yearly")
@my_permission("manager")
def stats_user_yearly():
    return jsonify(user_service.count_by_year())
from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from app.schemas.user import UserSchema

bp = Blueprint("users", __name__)
user_service = UserService()
user_schema = UserSchema()
users_schema = UserSchema(many=True)

@bp.route("/", methods=["GET"])
def get_users():
    users = user_service.get_all_users()
    return jsonify(users_schema.dump(users))

@bp.route("/", methods=["POST"])
def create_user():
    data = request.get_json()
    user = user_service.create_user(
        username=data["username"],
        email=data["email"]
    )
    return user_schema.dump(user), 201

@bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    user = user_service.update_user(
        user_id=user_id,
        username=data.get("username"),
        email=data.get("email")
    )
    if not user:
        return jsonify({"message": "User not found"}), 404
    return user_schema.dump(user)

@bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    success = user_service.delete_user(user_id)
    if not success:
        return jsonify({"message": "User not found"}), 404
    return jsonify({"message": "User deleted successfully"})

from flask import Blueprint, request, jsonify, g
from app.services.cart_service import CartService
from app.schemas.cart import (
    CartDetailSchema,
    CartItemCreateSchema,
    CartItemUpdateSchema,
)
from app.decorators.permissions import my_permission

bp = Blueprint("cart", __name__, url_prefix="/cart")
cart_service = CartService()

# Schema instances
cart_detail_schema = CartDetailSchema()
cart_item_create_schema = CartItemCreateSchema()
cart_item_update_schema = CartItemUpdateSchema()


# 1. Lấy giỏ hàng của user
@bp.route("/", methods=["GET"])
@my_permission(["user"])
def get_cart():
    user_id = g.current_user.id

    cart = cart_service.get_cart(user_id)
    if not cart:
        return jsonify({"message": "Cart is empty"}), 200

    return cart_detail_schema.dump(cart), 200


# 2. Thêm item vào giỏ
@bp.route("/items", methods=["POST"])
@my_permission(["user"])
def add_item():
    user_id = g.current_user.id
    data = request.get_json()

    errors = cart_item_create_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    try:
        cart = cart_service.add_item(
            user_id=user_id,
            event_id=data["event_id"],
            ticket_type=data["ticket_type"],
            quantity=data["quantity"],
        )
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return cart_detail_schema.dump(cart), 201


# 3. Update số lượng item
@bp.route("/items/<int:item_id>", methods=["PUT"])
@my_permission(["user"])
def update_item(item_id):
    user_id = g.current_user.id
    data = request.get_json()

    errors = cart_item_update_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400

    try:
        cart = cart_service.update_item(
            user_id=user_id,
            item_id=item_id,
            quantity=data.get("quantity"),
        )
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return cart_detail_schema.dump(cart), 200


# 4. Xóa item khỏi giỏ
@bp.route("/items/<int:item_id>", methods=["DELETE"])
@my_permission(["user"])
def remove_item(item_id):
    user_id = g.current_user.id

    try:
        cart = cart_service.remove_item(user_id=user_id, item_id=item_id)
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return cart_detail_schema.dump(cart), 200

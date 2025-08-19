from app.extensions import db
from sqlalchemy.exc import IntegrityError
from app.models.cart import Cart, CartItem
from app.models.ticket import TicketType


class CartService:
    def get_cart(self, user_id: int):
        """Lấy giỏ hàng của user"""
        return Cart.query.filter_by(user_id=user_id).first()

    def add_item(self, **data):
        """Thêm item vào giỏ hàng (tạo cart nếu chưa có)"""
        user_id = data.get("user_id")
        event_id = data.get("event_id")
        ticket_type = data.get("ticket_type")
        quantity = data.get("quantity")

        if not user_id or not event_id or not ticket_type:
            raise ValueError("Missing required fields: user_id, event_id, ticket_type")
        if quantity is None or quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        # Chuyển string -> Enum
        try:
            ticket_enum = TicketType[ticket_type]
        except KeyError:
            raise ValueError(f"Invalid ticket_type: {ticket_type}")

        cart = self.get_cart(user_id)
        if not cart:
            cart = Cart(user_id=user_id)
            db.session.add(cart)
            db.session.flush()  # để có cart.id

        # Kiểm tra item đã tồn tại
        existing_item = CartItem.query.filter_by(
            cart_id=cart.id,
            event_id=event_id,
            ticket_type=ticket_enum
        ).first()

        if existing_item:
            existing_item.quantity += quantity
        else:
            new_item = CartItem(
                cart_id=cart.id,
                event_id=event_id,
                ticket_type=ticket_enum,
                quantity=quantity
            )
            db.session.add(new_item)

        try:
            db.session.commit()
            return cart
        except IntegrityError as e:
            raise ValueError(f"Failed to add item: {str(e)}")

    def update_item(self, **data):
        """Cập nhật số lượng item (nếu =0 thì xóa)"""
        user_id = data.get("user_id")
        item_id = data.get("item_id")
        quantity = data.get("quantity")

        cart = self.get_cart(user_id)
        if not cart:
            raise ValueError("Cart not found")

        item = CartItem.query.filter_by(id=item_id, cart_id=cart.id).first()
        if not item:
            raise ValueError("Item not found in cart")

        if quantity <= 0:
            db.session.delete(item)
        else:
            item.quantity = quantity

        try:
            db.session.commit()
            return cart
        except Exception as e:
            raise Exception(f"Failed to update item: {str(e)}")

    def remove_item(self, **data):
        """Xóa 1 item khỏi giỏ hàng"""
        user_id = data.get("user_id")
        item_id = data.get("item_id")

        if not user_id or not item_id:
            raise ValueError("Missing required fields: user_id, item_id")

        cart = self.get_cart(user_id)
        if not cart:
            raise ValueError("Cart not found")

        item = CartItem.query.filter_by(id=item_id, cart_id=cart.id).first()
        if not item:
            raise ValueError("Item not found in cart")

        db.session.delete(item)
        try:
            db.session.commit()
            return cart
        except Exception as e:
            raise Exception(f"Failed to remove item: {str(e)}")

from app.extensions import db
from sqlalchemy.exc import IntegrityError
from app.models.cart import Cart, CartItem
from app.models.ticket import TicketType


class CartService:
    def get_cart(self, user_id: int):
        """Lấy giỏ hàng của user"""
        return Cart.query.filter_by(user_id=user_id).first()

    def add_item(self, user_id: int, event_id: int, ticket_type: str, quantity: int):
        """Thêm item vào giỏ hàng (tạo cart nếu chưa có)"""
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        # Chuyển string -> Enum
        try:
            ticket_enum = TicketType[ticket_type]  # "VIP" -> TicketType.VIP
        except KeyError:
            raise ValueError(f"Invalid ticket_type: {ticket_type}")

        cart = self.get_cart(user_id)
        if not cart:
            cart = Cart(user_id=user_id)
            db.session.add(cart)
            db.session.flush()  # để có cart.id

        # Kiểm tra nếu item cùng event_id + ticket_type đã tồn tại thì update quantity
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
            db.session.rollback()
            raise Exception(f"Failed to add item to cart: {str(e)}")

    def update_item(self, user_id: int, item_id: int, quantity: int):
        """Cập nhật số lượng item (nếu =0 thì xóa)"""
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
            db.session.rollback()
            raise Exception(f"Failed to update item: {str(e)}")

    def remove_item(self, user_id: int, item_id: int):
        """Xóa 1 item khỏi giỏ hàng"""
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
            db.session.rollback()
            raise Exception(f"Failed to remove item: {str(e)}")

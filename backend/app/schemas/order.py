from app.extensions import ma
from app.models.order import Order, OrderItem
from marshmallow import fields

# Base Schema cho OrderItem
class OrderItemSchema(ma.SQLAlchemyAutoSchema):
    ticket_id = fields.Int()
    price = fields.Float()

    class Meta:
        model = OrderItem
        load_instance = True
        include_fk = True
        exclude = ("order",)


# Base Schema cho Order
class OrderBaseSchema(ma.SQLAlchemyAutoSchema):
    items = fields.Nested(OrderItemSchema, many=True)

    class Meta:
        model = Order
        load_instance = True
        include_fk = True


# Input schema để tạo order
class OrderCreateSchema(ma.Schema):
    payment_method = fields.Str(required=True)
    items = fields.List(fields.Dict(), required=True)


# Output schema chi tiết order
class OrderDetailSchema(OrderBaseSchema):
    class Meta(OrderBaseSchema.Meta):
        exclude = ()

# Schema cho danh sách Order
class OrderListSchema(OrderBaseSchema):
    class Meta(OrderBaseSchema.Meta):
        fields = ("id", "status", "payment_method", "total_amount")
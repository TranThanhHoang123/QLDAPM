from app.extensions import ma
from app.models.order import Order, OrderItem, PaymentMethod
from app.schemas.user import UserListSchema
from app.schemas.ticket import TicketDetailSchema
from marshmallow import fields, validate

# Base Schema cho OrderItem
class OrderItemListSchema(ma.SQLAlchemyAutoSchema):
    ticket_id = fields.Int()
    price = fields.Float()
    ticket = fields.Nested(TicketDetailSchema)
    class Meta:
        model = OrderItem
        load_instance = True
        include_fk = True
        exclude = ("order",)


# Base Schema cho Order
class OrderBaseSchema(ma.SQLAlchemyAutoSchema):
    status = fields.Method("get_status")
    payment_method = fields.Method("get_payment_method")
    items = fields.Nested(OrderItemListSchema, many=True)

    class Meta:
        model = Order
        load_instance = True
        include_fk = True
    
    def get_status(self, obj):
        return obj.status.value if hasattr(obj.status, "value") else obj.status

    def get_payment_method(self, obj):
        return obj.payment_method.value if hasattr(obj.payment_method, "value") else obj.payment_method

# Input schema để tạo order
class OrderCreateSchema(ma.Schema):
    payment_method = fields.Str(
        required=True,
        validate=validate.OneOf([e.value for e in PaymentMethod])
    )
    items = fields.List(fields.Dict(), required=True)

# Output schema chi tiết order
class OrderDetailSchema(OrderBaseSchema):
    user = fields.Nested(UserListSchema)
    class Meta(OrderBaseSchema.Meta):
        exclude = ()

# Schema cho danh sách Order
class OrderListSchema(OrderBaseSchema):
    class Meta(OrderBaseSchema.Meta):
        fields = ("id", "status", "payment_method", "total_amount")

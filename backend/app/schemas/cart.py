from app.extensions import ma
from app.models.cart import Cart, CartItem
from app.models.ticket import TicketType
from app.schemas.event import EventListSchema
from marshmallow import fields, validate

class CartItemBaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CartItem
        load_instance = True
        include_fk = True   # để hiện event_id, cart_id

class CartBaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cart
        load_instance = True
        include_fk = True

class CartItemCreateSchema(CartItemBaseSchema):
    class Meta(CartItemBaseSchema.Meta):
        exclude = ("id", "cart_id")

    event_id = fields.Integer(required=True)
    ticket_type = fields.String(
        required=True,
        validate=validate.OneOf([e.value for e in TicketType])
    )
    quantity = fields.Integer(
        required=True,
        validate=validate.Range(min=1, error="Quantity must be greater than 0")
    )

class CartItemUpdateSchema(CartItemBaseSchema):
    quantity = fields.Integer(
        required=True,
        validate=validate.Range(min=1, error="Quantity must be greater than 0")
    )
    class Meta(CartItemBaseSchema.Meta):
        exclude = ("id", "cart_id", "event_id", "ticket_type")

class CartItemDetailSchema(CartItemBaseSchema):
    event = fields.Nested(EventListSchema)
    class Meta(CartItemBaseSchema.Meta):
        exclude = ()

class CartDetailSchema(CartBaseSchema):
    items = ma.Nested(CartItemDetailSchema, many=True)

    class Meta(CartBaseSchema.Meta):
        exclude = ()

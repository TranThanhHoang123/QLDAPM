from app.extensions import ma
from app.models import Ticket
from marshmallow import fields, validate
from flask import request
from app.schemas.user import UserListSchema
from app.schemas.event import EventListSchema
# Base Schema
class TicketBaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ticket
        load_instance = True
        include_fk = True
    

# 1. Create Ticket Schema
class TicketCreateSchema(TicketBaseSchema):
    class Meta(TicketBaseSchema.Meta):
        exclude = ("id", "status", "user_id",)

    event_id = fields.Integer(required=True)
    type = fields.String(
        required=True,
        validate=validate.OneOf(["VIP", "STANDARD"])
    )
    price = fields.Decimal(required=True, as_string=True)
    quantity = fields.Integer(
        required=True,
        validate=validate.Range(min=1, error="Quantity must be greater than 0")
    )


# 3. List Ticket Schema
class TicketListSchema(TicketBaseSchema):
    class Meta(TicketBaseSchema.Meta):
        exclude = ()


# 4. Detail Ticket Schema
class TicketDetailSchema(TicketBaseSchema):
    user = fields.Nested(UserListSchema)
    event = fields.Nested(EventListSchema)
    class Meta(TicketBaseSchema.Meta):
        exclude = ()

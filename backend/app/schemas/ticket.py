from app.extensions import ma
from app.models.ticket import Ticket, TicketType
from marshmallow import fields, validate
from app.schemas.user import UserListSchema
from app.schemas.event import EventListSchema
# Base Schema
class TicketBaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ticket
        load_instance = True
        include_fk = True
    
class TicketCreateSchema(TicketBaseSchema):
    class Meta(TicketBaseSchema.Meta):
        exclude = ("id", "status", "user_id",)

    event_id = fields.Integer(required=True)
    type = fields.String(
        required=True,
        validate=validate.OneOf([e.value for e in TicketType])
    )
    price = fields.Decimal(required=True, as_string=True)
    quantity = fields.Integer(
        required=True,
        validate=validate.Range(min=1, error="Quantity must be greater than 0")
    )

class TicketListSchema(TicketBaseSchema):
    event = fields.Nested(EventListSchema)
    class Meta(TicketBaseSchema.Meta):
        exclude = ()

class TicketDetailSchema(TicketBaseSchema):
    user = fields.Nested(UserListSchema)
    event = fields.Nested(EventListSchema)
    class Meta(TicketBaseSchema.Meta):
        exclude = ()

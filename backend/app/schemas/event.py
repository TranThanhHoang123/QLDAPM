from app.extensions import ma
from app.models import Event
from marshmallow import fields, validate
from flask import request
from app.schemas.category import CategoryListSchema
from app.models.ticket import TicketStatus, TicketType

# Base Schema
class EventBaseSchema(ma.SQLAlchemyAutoSchema):
    # Format datetime khi dump/load
    start_time = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    end_time = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    image = fields.Method("get_image")
    category = fields.Nested(CategoryListSchema)
    available_ticket_counts = fields.Method("get_available_ticket_counts")

    class Meta:
        model = Event
        load_instance = True
        include_fk = True  # Để hiển thị category_id

    def get_image(self, obj):
        if not obj.image:
            return None
        # domain hiện tại
        base_url = request.host_url.rstrip("/")
        # trả về full url
        return f"{base_url}/static/{obj.image}"
    
    def get_available_ticket_counts(self, obj):
        counts = {t.value: 0 for t in TicketType}
        for ticket in obj.tickets:
            if ticket.status == TicketStatus.AVAILABLE:
                counts[ticket.type.value] += 1
        return counts


# 1. Create Event Schema
class EventCreateSchema(EventBaseSchema):
    title = fields.String(required=True, validate=validate.Length(min=1, max=200))
    location = fields.String(validate=validate.Length(max=200))
    category_id = fields.Integer(required=True)

    class Meta(EventBaseSchema.Meta):
        exclude = ("id", "image")


# 2. Update Event Schema
class EventUpdateSchema(EventBaseSchema):
    title = fields.String(validate=validate.Length(min=1, max=200))
    location = fields.String(validate=validate.Length(max=200))
    category_id = fields.Integer()

    class Meta(EventBaseSchema.Meta):
        exclude = ("id", "image")


# 3. List Event Schema
class EventListSchema(EventBaseSchema):
    class Meta(EventBaseSchema.Meta):
        exclude = ("description",)


# 4. Detail Event Schema
class EventDetailSchema(EventBaseSchema):
    class Meta(EventBaseSchema.Meta):
        exclude = ()

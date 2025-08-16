from app.extensions import ma
from app.models import Event
from marshmallow import fields
from flask import request
from app.schemas.category import CategoryListSchema
# Base Schema
class EventBaseSchema(ma.SQLAlchemyAutoSchema):
    # Format datetime khi dump/load
    start_time = ma.DateTime(format="%Y-%m-%d %H:%M:%S")
    end_time   = ma.DateTime(format="%Y-%m-%d %H:%M:%S")
    image = fields.Method("get_image")
    category = fields.Nested(CategoryListSchema)
    class Meta:
        model = Event
        load_instance = True
        include_fk = True   # Để hiển thị category_id
    
    def get_image(self, obj):
        if not obj.image:
            return None
        # domain hiện tại
        base_url = request.host_url.rstrip("/")  
        # trả về full url
        return f"{base_url}/static/{obj.image}"


# 1. Create Event Schema
class EventCreateSchema(EventBaseSchema):
    class Meta(EventBaseSchema.Meta):
        exclude = ("id", "image")


# 2. Update Event Schema
class EventUpdateSchema(EventBaseSchema):
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

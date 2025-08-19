from app.extensions import ma
from app.models.user import User
from marshmallow import fields, validate
# Base schema
class UserBaseSchema(ma.SQLAlchemyAutoSchema):
    role = fields.Method("get_role")
    class Meta:
        model = User
        load_instance = True
        include_fk = True
    
    def get_role(self, obj):
        # Nếu obj.role là Enum trả value, nếu không trả luôn
        return obj.role.value if hasattr(obj.role, "value") else obj.role

class UserCreateSchema(UserBaseSchema):
    username = fields.String(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=6))
    phone_number = fields.String(required=True, validate=validate.Length(min=1))

    class Meta(UserBaseSchema.Meta):
        exclude = ("id", "role", "created_at", "updated_at")

class UserUpdateSchema(UserBaseSchema):
    email = fields.Email()
    phone_number = fields.String(validate=validate.Length(min=1))
    class Meta(UserBaseSchema.Meta):
        exclude = ("id","username", "role", "password", "created_at", "updated_at")

class UserChangePasswordSchema(ma.Schema):
    old_password = fields.String(required=True)
    new_password = fields.String(required=True, load_only=True, validate=validate.Length(min=6))

class UserListSchema(UserBaseSchema):
    class Meta(UserBaseSchema.Meta):
        exclude = ("created_at", "updated_at", "password")

class UserDetailSchema(UserBaseSchema):
    class Meta(UserBaseSchema.Meta):
        exclude = ("password", "username")
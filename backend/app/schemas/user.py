from app.extensions import ma
from app.models.user import User
from marshmallow import fields
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

# Serializer for user

# 1. Create User Schema
class UserCreateSchema(UserBaseSchema):
    class Meta(UserBaseSchema.Meta):
        exclude = ("id", "role", "created_at", "updated_at")

# 2. Update User Schema
class UserUpdateSchema(UserBaseSchema):
    class Meta(UserBaseSchema.Meta):
        exclude = ("username", "password", "created_at", "updated_at")

class UserChangePasswordSchema(ma.Schema):
    old_password = ma.String(required=True)
    new_password = ma.String(required=True)

class UserListSchema(UserBaseSchema):
    class Meta(UserBaseSchema.Meta):
        exclude = ("created_at", "updated_at", "password")

class UserDetailSchema(UserBaseSchema):
    class Meta(UserBaseSchema.Meta):
        exclude = ("password", "username")
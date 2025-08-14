from app.extensions import ma
from app.models.user import User

# Serializer for user
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True

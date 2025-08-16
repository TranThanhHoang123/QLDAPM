from app.extensions import ma
from app.models import Category

# Base schema
class CategoryBaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True


# 1. Create Category Schema
class CategoryCreateSchema(CategoryBaseSchema):
    class Meta(CategoryBaseSchema.Meta):
        exclude = ("id",)


# 2. Update Category Schema
class CategoryUpdateSchema(CategoryBaseSchema):
    class Meta(CategoryBaseSchema.Meta):
        exclude = ("id",)


# 3. List Category Schema
class CategoryListSchema(CategoryBaseSchema):
    class Meta(CategoryBaseSchema.Meta):
        exclude = ("description",)


# 4. Detail Category Schema
class CategoryDetailSchema(CategoryBaseSchema):
    class Meta(CategoryBaseSchema.Meta):
        exclude = ()
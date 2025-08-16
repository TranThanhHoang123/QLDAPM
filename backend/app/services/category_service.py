from app.extensions import db
from app.models.category import Category
from datetime import datetime
from sqlalchemy.exc import IntegrityError

class CategoryService:
    def get_categories(self, **kwargs):
        query = Category.query

        # Lọc theo tên
        if "name" in kwargs and kwargs["name"]:
            query = query.filter(Category.name.ilike(f"%{kwargs['name']}%"))

        try:
            page = int(kwargs.get("page", 1))
        except ValueError:
            page = 1

        try:
            page_size = int(kwargs.get("page_size", 10))
        except ValueError:
            page_size = 10

        # Phân trang
        pagination = query.paginate(page=page, per_page=page_size, error_out=False)
        return pagination
    
    def get_category(self, category_id):
        return Category.query.get(category_id)

    def create_category(self, **data):
        category = Category(**data)
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            raise ValueError("Category name already exists")
        return category, None

    def update_category(self, category_id, **data):
        category = Category.query.get(category_id)
        if not category:
            raise ValueError("Category not found")

        disallowed = {"id"}
        for field, value in data.items():
            if field not in disallowed and hasattr(category, field) and value is not None:
                setattr(category, field, value)

        try:
            db.session.commit()
            return category
        except IntegrityError:
            raise ValueError("Category name already exists")
        except Exception as e:
            raise Exception(f"Failed to update category: {str(e)}")

    def delete_category(self, category_id):
        category = Category.query.get(category_id)
        if not category:
            raise ValueError("Category not found")
        
        try:
            db.session.delete(category)
            db.session.commit()
            return True
        except Exception as e:
            raise Exception(f"Failed to delete category: {str(e)}")
    



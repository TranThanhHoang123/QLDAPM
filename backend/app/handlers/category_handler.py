from flask import Blueprint, request, jsonify
from app.services.category_service import CategoryService
from app.decorators.permissions import my_permission
from app.schemas.category import (
    CategoryCreateSchema,
    CategoryUpdateSchema,
    CategoryListSchema,
    CategoryDetailSchema
)

bp = Blueprint("categories", __name__, url_prefix="/categories")
category_service = CategoryService()

# Schema instances
category_create_schema = CategoryCreateSchema()
category_update_schema = CategoryUpdateSchema()
category_list_schema = CategoryListSchema(many=True)
category_detail_schema = CategoryDetailSchema()


# 1. Lấy danh sách category
@bp.route("/", methods=["GET"])
def get_categories():
    params = request.args.to_dict()
    pagination = category_service.get_categories(**params)

    return jsonify({
        "items": category_list_schema.dump(pagination.items),
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages,
    })


# 2. Lấy chi tiết category
@bp.route("/<int:category_id>", methods=["GET"])
def get_category(category_id):
    category = category_service.get_category(category_id)
    if not category:
        return jsonify({"message": "Category not found"}), 404
    return category_detail_schema.dump(category), 200


# 3. Tạo category
@bp.route("/", methods=["POST"])
@my_permission("manager")
def create_category():
    data = request.get_json()
    errors = category_create_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    try:
        category = category_service.create_category(**data)
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return category_detail_schema.dump(category), 201


# 4. Cập nhật category
@bp.route("/<int:category_id>", methods=["PUT"])
@my_permission("manager")
def update_category(category_id):
    data = request.get_json()
    errors = category_update_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400

    try:
        category = category_service.update_category(category_id, **data)
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    if not category:
        return jsonify({"message": "Category not found"}), 404

    return category_detail_schema.dump(category), 200


# 5. Xóa category
@bp.route("/<int:category_id>", methods=["DELETE"])
@my_permission("admin")
def delete_category(category_id):
    try:
        category_service.delete_category(category_id)
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "Category deleted successfully"}), 200

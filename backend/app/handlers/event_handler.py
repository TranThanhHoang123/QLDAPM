from flask import Blueprint, request, jsonify
from app.services.event_service import EventService
from app.decorators.permissions import my_permission
from app.schemas.event import (
    EventCreateSchema,
    EventUpdateSchema,
    EventListSchema,
    EventDetailSchema
)
from app.utils.helpers import save_image

bp = Blueprint("events", __name__, url_prefix="/event")
event_service = EventService()

# Schema instances
event_create_schema = EventCreateSchema()
event_update_schema = EventUpdateSchema()
event_list_schema = EventListSchema(many=True)
event_detail_schema = EventDetailSchema()


# 1. Lấy danh sách event
@bp.route("/", methods=["GET"])
def get_events():
    params = request.args.to_dict()
    pagination = event_service.get_events(**params)

    return jsonify({
        "items": event_list_schema.dump(pagination.items),
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages
    })


# 2. Lấy chi tiết event
@bp.route("/<int:event_id>", methods=["GET"])
def get_event(event_id):
    event = event_service.get_event(event_id)
    if not event:
        return jsonify({"message": "Event not found"}), 404
    return event_detail_schema.dump(event), 200


# 3. Tạo event
@bp.route("/", methods=["POST"])
@my_permission("manager")
def create_event():
    data = request.form.to_dict()
    file = request.files.get("image")

    errors = event_create_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    if file:
        data["image"] = save_image(file, "events")

    event = event_service.create_event(**data)

    return event_detail_schema.dump(event), 201


# 4. Cập nhật event
@bp.route("/<int:event_id>", methods=["PUT", "PATCH"])
@my_permission("manager")
def update_event(event_id):
    data = request.form.to_dict()
    file = request.files.get("image")

    # validate input
    errors = event_update_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Nếu có file mới -> thay ảnh
    if file:
        data["image"] = save_image(file, "events")

    try:
        event = event_service.update_event(event_id, **data)
    except ValueError as e:
        return jsonify({"message": str(e)}), 404
    except Exception as e:
        return jsonify({"message": f"Error updating event: {str(e)}"}), 400

    return event_detail_schema.dump(event), 200


# 5. Xóa event
@bp.route("/<int:event_id>", methods=["DELETE"])
@my_permission("admin")
def delete_event(event_id):
    try:
        success = event_service.delete_event(event_id)
        if not success:
            return jsonify({"message": "Event not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "Event deleted successfully"}), 200

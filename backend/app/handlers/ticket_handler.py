from flask import Blueprint, request, jsonify
from app.services.ticket_service import TicketService
from app.services.event_service import EventService
from app.decorators.permissions import my_permission
from app.schemas.ticket import (
    TicketCreateSchema,
    TicketListSchema,
    TicketDetailSchema
)

bp = Blueprint("tickets", __name__, url_prefix="/ticket")
ticket_service = TicketService()
event_service = EventService()

# Schema instances
ticket_create_schema = TicketCreateSchema()
ticket_list_schema = TicketListSchema(many=True)
ticket_detail_schema = TicketDetailSchema()


# 1. Lấy danh sách vé (có filter + phân trang)
@bp.route("/", methods=["GET"])
@my_permission(["manager"])
def get_tickets():
    params = request.args.to_dict()
    pagination = ticket_service.get_tickets(**params)

    return jsonify({
        "items": ticket_list_schema.dump(pagination.items),
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages
    })


# 2. Lấy chi tiết vé
@bp.route("/<int:ticket_id>", methods=["GET"])
@my_permission(["manager"])
def get_ticket_for_manager(ticket_id):
    ticket = ticket_service.get_ticket(ticket_id)
    if not ticket:
        return jsonify({"message": "Ticket not found"}), 404
    return ticket_detail_schema.dump(ticket), 200


# 3. Tạo vé (manager hoặc admin thêm vé cho sự kiện)
@bp.route("/", methods=["POST"])
@my_permission(["manager"])
def create_tickets():
    data = request.get_json()

    errors = ticket_create_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    event_id = data["event_id"]
    ticket_type = data["type"]
    price = float(data["price"])
    quantity = int(data["quantity"])

     # Check event tồn tại
    event = event_service.get_event(event_id)
    if not event:
        return jsonify({"message": "event not found"}), 404
    
    tickets = ticket_service.create_tickets(event_id, ticket_type, price, quantity)

    return ticket_list_schema.dump(tickets), 201

from flask import Blueprint, g, jsonify,  request, redirect
from app.services.order_service import OrderService
from app.decorators.permissions import my_permission
from datetime import datetime
from app.utils.vnpay import vnpay
from app.utils.momo import create_payment
from app.utils.jwt import JwtUtil
from app.schemas.order import (
    OrderCreateSchema,
    OrderListSchema,
    OrderDetailSchema
)

bp = Blueprint("orders", __name__, url_prefix="/orders")
order_service = OrderService()
jwt_util = JwtUtil()
# Schema instances
order_create_schema = OrderCreateSchema()
order_detail_schema = OrderDetailSchema()
order_list_schema = OrderListSchema()

VNPAY_URL = "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html"
VNPAY_TMNCODE = "LZPLRB1E"
VNPAY_HASH_SECRET = "APBHTE4INVHF4PE8N0DBU6G09NHAMWQU"
VNPAY_RETURN_URL = "http://localhost:8080/vnpay/payment_return"

# 1. Tạo order
@bp.route("/", methods=["POST"])
@my_permission(["user"])
def create_order():
    data = request.get_json()
    errors = order_create_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    user_id = g.current_user.id
    payment_method = data["payment_method"]
    items = data["items"]

    order, error = order_service.create_order(user_id, payment_method, items)
    if error:
        return jsonify({"error": error}), 400
    
    # 2.1 Nếu chọn VNPAY thì tạo link payment
    if payment_method == "vnpay":
        # Lấy domain backend hiện tại, vd: http://127.0.0.1:5000/
        current_domain = request.host_url.rstrip("/")  
        VNPAY_RETURN_URL = f"{current_domain}/orders/vnpay/payment_return"
        vnp = vnpay()
        vnp.requestData = {
            'vnp_Version': '2.1.0',
            'vnp_Command': 'pay',
            'vnp_TmnCode': VNPAY_TMNCODE,
            'vnp_Amount': str(int(order.total_amount) * 100),  # VND * 100
            'vnp_CurrCode': 'VND',
            'vnp_TxnRef': str(order.id),  # dùng order.id làm mã tham chiếu
            'vnp_OrderInfo': f"Thanh toan don hang {order.id}",
            'vnp_OrderType': 'other',
            'vnp_Locale': 'vn',
            'vnp_CreateDate': datetime.now().strftime('%Y%m%d%H%M%S'),
            'vnp_IpAddr': request.remote_addr,
            'vnp_ReturnUrl': VNPAY_RETURN_URL
        }
        payment_url = vnp.get_payment_url(VNPAY_URL, VNPAY_HASH_SECRET)

        return jsonify({
            "order": order_detail_schema.dump(order),
            "payment_url": payment_url
        }), 201

    # 2.2 Nếu chọn MOMO thì thanh toán bằng momo
    if payment_method == "momo":
        current_domain = request.host_url.rstrip("/")
        MOMO_RETURN_URL = f"{current_domain}/orders/momo/payment_return"

        # gọi utils để tạo payment
        momo_response = create_payment(
            amount=str(order.total_amount),
            order_id=str(order.id),          # dùng order.id làm orderId
            return_url=MOMO_RETURN_URL       # truyền return url động
        )

        # MoMo trả về payUrl để redirect
        pay_url = momo_response.get("payUrl")

        return jsonify({
            "order": order_detail_schema.dump(order),
            "payment_url": pay_url
        }), 201

    # Nếu thanh toán offline thì trả về luôn
    return jsonify(order_detail_schema.dump(order)), 201

# 2.1 Xử lý thanh toán vnpay
@bp.route("/vnpay/payment_return", methods=["GET"])
def vnpay_return():
    query_params = request.args.to_dict()

    order_id = query_params.get("vnp_TxnRef")
    transaction_status = query_params.get("vnp_TransactionStatus")

    if not order_id:
        return jsonify({"error": "Invalid return data"}), 400

    if transaction_status == "00":  # Thanh toán thành công
        order, error = order_service.payment_success(order_id)
    else:
        order, error = order_service.payment_failed(order_id)

    if error:
        return jsonify({"error": error}), 400

    # Redirect sang FE, kèm trạng thái
    redirect_url = f"http://localhost:3000/payment_result?order_id={order.id}&status={order.status}"
    return redirect(redirect_url)

# 2.2 Xử lý thanh toán momo
@bp.route("/momo/payment_return", methods=["GET"])
def momo_return():
    print("/momo/payment_return")
    query_params = request.args.to_dict()
    print("query_params", query_params)

    order_id_raw = query_params.get("orderId")
    result_code = query_params.get("resultCode")  # 0 = success
    if not order_id_raw:
        return jsonify({"error": "Invalid return data"}), 400

    # Tách orderId gốc (bỏ phần timestamp)
    order_id = order_id_raw.split("_")[0]

    if result_code == "0":
        # Thanh toán thành công
        order, error = order_service.payment_success(order_id)
    else:
        # Thanh toán thất bại
        order, error = order_service.payment_failed(order_id)

    # Nếu có lỗi thì trả về ngay
    if error:
        return jsonify({"error": error}), 400

    # Redirect sang FE, kèm trạng thái
    redirect_url = f"http://localhost:3000/payment_result?order_id={order.id}&status={order.status}"
    return redirect(redirect_url)

# 4. Xem chi tiết order
@bp.route("/<int:order_id>", methods=["GET"])
@my_permission(["manager"])
def get_order_detail_for_manager(order_id):
    order = order_service.get_order(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    return jsonify(order_detail_schema.dump(order)), 200

# 3. Xem chi tiết order của user
@bp.route("/me/<int:order_id>", methods=["GET"])
@my_permission(["user"])
def get_order_detail(order_id):
    order = order_service.get_order(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    # Chỉ cho phép xem order của chính user
    if order.user_id != g.current_user.id and g.current_user.role.value == "user":
        return jsonify({"error": "Permission denied"}), 403

    return jsonify(order_detail_schema.dump(order)), 200

# 5. Lấy danh sách order cho quản lý
@bp.route("/", methods=["GET"])
@my_permission(["manager"])
def get_orders_for_manager():
    params = request.args.to_dict()
    pagination = order_service.get_orders(**params)

    return jsonify({
        "items": order_list_schema.dump(pagination.items),
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages
    })

# 6. Lấy danh sách order cho chính user
@bp.route("/me", methods=["GET"])
@my_permission(["user"])
def get_orders():
    params = request.args.to_dict()
    pagination = order_service.get_orders(**params)

    # Thêm user id
    params["user_id"] = g.current_user.id

    return jsonify({
        "items": order_list_schema.dump(pagination.items),
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages
    })
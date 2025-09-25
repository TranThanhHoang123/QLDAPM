// src/services/orderService.js
import apiClient from "./apiClient";

const orderService = {
  // Tạo đơn hàng
  createOrder: (data) =>
    apiClient.post("/orders/", {
      payment_method: data.payment_method, // "MOMO" hoặc "VNPAY"
      items: data.items, // [{ event_id, ticket_type, quantity }]
    }),

  // Lấy chi tiết 1 order của user hiện tại
  getOrderDetail: (orderId) => apiClient.get(`/orders/me/${orderId}`),

  // Lấy danh sách order của user hiện tại (có thể filter theo status, payment_method, page, page_size)
  getOrderList: (params) => apiClient.get("/orders/me", { params }),
};

export default orderService;

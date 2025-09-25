import apiClient from "./apiClient";

const cartService = {
  // Lấy danh sách giỏ hàng, có thể query theo name
  getList: (params) => apiClient.get("/cart/", { params }),

  // Thêm vé vào giỏ
  addTicket: (data) =>
    apiClient.post("/cart/items", {
      event_id: data.event_id,
      ticket_type: data.ticket_type, // "VIP" hoặc "STANDARD"
      quantity: data.quantity,
    }),

  // Cập nhật số lượng vé trong giỏ
  updateQuantityTicket: (itemId, quantity) =>
    apiClient.put(`/cart/items/${itemId}`, { quantity }),

  // Xóa vé khỏi giỏ
  removeTicket: (itemId) => apiClient.delete(`/cart/items/${itemId}`),
};

export default cartService;

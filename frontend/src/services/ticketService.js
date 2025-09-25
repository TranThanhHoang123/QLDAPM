// src/services/ticketService.js
import apiClient from "./apiClient";

const ticketService = {
  // Tạo ticket mới cho 1 event
  createTicket: (data) =>
    apiClient.post("/ticket/", {
      event_id: data.event_id,
      type: data.type, // "VIP" | "STANDARD"
      price: data.price,
      quantity: data.quantity,
    }),

  // Lấy chi tiết ticket (dành cho manager)
  getTicketDetailForManager: (ticketId) =>
    apiClient.get(`/ticket/${ticketId}`),

  // Lấy danh sách ticket cho manager
  // filter: { page, page_size, event_id, type, status }
  getTicketListForManager: (params) =>
    apiClient.get("/ticket/", { params }),

  // Lấy chi tiết 1 ticket của user hiện tại
  getTicketDetail: (ticketId) =>
    apiClient.get(`/ticket/me/${ticketId}`),

  // Lấy danh sách ticket của user hiện tại
  // filter: { page, page_size, type, status }
  getTicketList: (params) =>
    apiClient.get("/ticket/me", { params }),
};

export default ticketService;

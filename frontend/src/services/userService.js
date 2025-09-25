import apiClient from "./apiClient";

const userService = {
  login: (username, password) =>
    apiClient.post("/user/login", { username, password }),

  register: (username, password, name, email, phone_number) =>
    apiClient.post("/user/register", { username, password, name, email, phone_number }),

  getCurrentProfile: () =>
    apiClient.get("/user/me"),

  updateProfile: (data) =>
    apiClient.put("/user/me", data), // { name, email, phone_number }

  changePassword: (old_password, new_password) =>
    apiClient.put("/user/me/change-password", {old_password, new_password}),

  getList: (params) => apiClient.get("/user/", { params }),
  createManager: (data) => apiClient.post("/user/", data),
};

export default userService;

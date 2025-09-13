import axios from "axios";

const apiClient = axios.create({
  baseURL: "https://qldapm-backend-latest.onrender.com", // đổi theo backend của bạn
  headers: {
    "Content-Type": "application/json",
  },
});

// Optional: interceptor để tự động đính token vào request
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default apiClient;
import axios from "axios";

const apiClient = axios.create({
  baseURL: "https://qldapm-backend-latest.onrender.com", // đổi theo backend của bạn
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor: tự động gắn token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor: bắt 401 redirect login (nếu không ở trang login)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem("token");
      if (window.location.pathname !== "/login") {
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export default apiClient;

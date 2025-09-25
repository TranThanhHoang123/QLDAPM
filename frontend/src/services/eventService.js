import apiClient from "./apiClient";

const eventService = {
  getList: (params = {}) => {
    const defaultParams = {
      page: 1,
      page_size: 10,
    };
    return apiClient.get("/event/", {
      params: { ...defaultParams, ...params },
    });
  },
  getDetail: (id) =>
    apiClient.get(`/event/${id}`),

  update: (id, data) => {
    const formData = new FormData()
    Object.keys(data).forEach((key) => {
      if (data[key] !== undefined && data[key] !== null) {
        formData.append(key, data[key])
      }
    })
    return apiClient.put(`/event/${id}`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    })
  },
  create: (data) => {
    const formData = new FormData()
    Object.keys(data).forEach((key) => {
      if (data[key] !== undefined && data[key] !== null) {
        formData.append(key, data[key])
      }
    })
    return apiClient.post(`/event/`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    })
  },
}
export default eventService;
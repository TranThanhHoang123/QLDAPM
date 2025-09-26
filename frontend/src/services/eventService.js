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
async create(data) {
  console.log("eventService.create input data:", data)

  if (data instanceof FormData) {
    console.log("eventService.create sending FormData")
    for (let [key, value] of data.entries()) {
      console.log("->", key, value)
    }
  } else {
    console.log("eventService.create sending JSON:", data)
  }

  return apiClient.post("/event/", data, {
    headers: data instanceof FormData ? { "Content-Type": "multipart/form-data" } : {}
  })
}


}
export default eventService;
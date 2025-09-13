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
}
export default eventService;
import apiClient from "./apiClient";

const categoryService = {
  getList: () =>
    apiClient.get("/categories/"),
}
export default categoryService;
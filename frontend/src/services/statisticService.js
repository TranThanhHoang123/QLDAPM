import apiClient from "./apiClient";

const statisticService = {
  getMonthlyCustomerStatistic: (year) =>
    apiClient.get(`/user/stats/monthly/${year}`),
  getQuarterlyCustomerStatistic: (year) =>
    apiClient.get(`/user/stats/quarterly/${year}`),
  getYearlyCustomerStatistic: () =>
    apiClient.get(`/user/stats/yearly`),

  getMonthlyOrdersStatistic: (year) =>
    apiClient.get(`/orders/stats/monthly/${year}`),
  getQuarterlyOrdersStatistic: (year) =>
    apiClient.get(`/orders/stats/quarterly/${year}`),
  getYearlyOrdersStatistic: () =>
    apiClient.get(`/orders/stats/yearly`),

  getMonthlyTicketsStatistic: (year) =>
    apiClient.get(`/ticket/stats/monthly/${year}`),
  getQuarterlyTicketsStatistic: (year) =>
    apiClient.get(`/ticket/stats/quarterly/${year}`),
  getYearlyTicketsStatistic: () =>
    apiClient.get(`/ticket/stats/yearly`),
}

export default statisticService;
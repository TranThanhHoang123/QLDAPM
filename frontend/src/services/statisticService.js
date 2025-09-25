import apiClient from "./apiClient";

const statisticService = {
  getMonthlyCustomerStatistic: (year) =>
    apiClient.get(`/user/stats/monthly/${year}`),
  getQuarterlyCustomerStatistic: (year) =>
    apiClient.get(`/user/stats/quarterly/${year}`),
  getYearlyCustomerStatistic: () =>
    apiClient.get(`/user/stats/yearly/`),

  getMonthlyOrdersStatistic: (year) =>
    apiClient.get(`/orders/stats/monthly/${year}`),
  getQuarterlyOrdersStatistic: (year) =>
    apiClient.get(`/orders/stats/quarterly/${year}`),
  getYearlyOrdersStatistic: () =>
    apiClient.get(`/orders/stats/yearly/`),

  getMonthlyTicketStatistic: (year) =>
    apiClient.get(`/ticket/stats/monthly/${year}`),
  getQuarterlyTicketStatistic: (year) =>
    apiClient.get(`/ticket/stats/quarterly/${year}`),
  getYearlyTicketStatistic: () =>
    apiClient.get(`/ticket/stats/yearly/`),
}

export default statisticService;
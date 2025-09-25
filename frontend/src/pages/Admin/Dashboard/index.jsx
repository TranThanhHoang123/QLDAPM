import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { useEffect, useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  XAxis, YAxis, Tooltip, CartesianGrid, Legend, ResponsiveContainer
} from "recharts"
import statisticService from "../../../services/statisticService"

const COLORS = ["#6366f1", "#22c55e", "#f59e0b", "#ef4444", "#14b8a6"]

function Dashboard() {
  const [activeTab, setActiveTab] = useState("customers") // customers | orders | tickets
  const [chartType, setChartType] = useState("bar") // bar | line | pie
  const [statType, setStatType] = useState("monthly") // monthly | quarterly | yearly
  const [year, setYear] = useState(new Date().getFullYear())
  const [data, setData] = useState([])
  const [pieMetric, setPieMetric] = useState("orders") // orders | revenue (chỉ dùng cho Orders Pie)

  // fetch data
  useEffect(() => {
    async function fetchData() {
      try {
        let res
        if (activeTab === "customers") {
          if (statType === "monthly") res = await statisticService.getMonthlyCustomerStatistic(year)
          else if (statType === "quarterly") res = await statisticService.getQuarterlyCustomerStatistic(year)
          else res = await statisticService.getYearlyCustomerStatistic()
        } else if (activeTab === "orders") {
          if (statType === "monthly") res = await statisticService.getMonthlyOrdersStatistic(year)
          else if (statType === "quarterly") res = await statisticService.getQuarterlyOrdersStatistic(year)
          else res = await statisticService.getYearlyOrdersStatistic()
        } else if (activeTab === "tickets") {
          if (statType === "monthly") res = await statisticService.getMonthlyTicketsStatistic(year)
          else if (statType === "quarterly") res = await statisticService.getQuarterlyTicketsStatistic(year)
          else res = await statisticService.getYearlyTicketsStatistic()
        }
        setData(res.data || [])
      } catch (err) {
        console.error("Fetch stats failed", err)
      }
    }
    fetchData()
  }, [activeTab, statType, year])

  const xKey = statType === "monthly" ? "month" : statType === "quarterly" ? "quarter" : "year"

  const renderChart = () => {
    if (chartType === "bar") {
      return (
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={xKey} />
          <YAxis />
          <Tooltip />
          <Legend />
          {activeTab === "orders" ? (
            <>
              <Bar dataKey="orders" fill="#6366f1" name="Số đơn" />
              <Bar dataKey="revenue" fill="#22c55e" name="Doanh thu" />
            </>
          ) : (
            <Bar
              dataKey="count"
              fill="#6366f1"
              name={activeTab === "tickets" ? "Số vé" : "Số KH"}
            />
          )}
        </BarChart>
      )
    }

    if (chartType === "line") {
      return (
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={xKey} />
          <YAxis />
          <Tooltip />
          <Legend />
          {activeTab === "orders" ? (
            <>
              <Line type="monotone" dataKey="orders" stroke="#6366f1" name="Số đơn" />
              <Line type="monotone" dataKey="revenue" stroke="#22c55e" name="Doanh thu" />
            </>
          ) : (
            <Line
              type="monotone"
              dataKey="count"
              stroke="#22c55e"
              name={activeTab === "tickets" ? "Số vé" : "Số KH"}
            />
          )}
        </LineChart>
      )
    }

    if (chartType === "pie") {
      const pieKey =
        activeTab === "orders"
          ? pieMetric
          : activeTab === "tickets"
          ? "count"
          : "count"

      return (
        <PieChart>
          <Tooltip />
          <Legend />
          <Pie
            data={data}
            dataKey={pieKey}
            nameKey={xKey}
            cx="50%"
            cy="50%"
            outerRadius={120}
            label
          >
            {data.map((_, idx) => (
              <Cell key={idx} fill={COLORS[idx % COLORS.length]} />
            ))}
          </Pie>
        </PieChart>
      )
    }
  }

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-2xl font-bold">Dashboard</h1>

      {/* Bộ chọn */}
      <div className="flex flex-wrap gap-4">
        <Select value={activeTab} onValueChange={setActiveTab}>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Chọn Dashboard" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="customers">Khách hàng</SelectItem>
            <SelectItem value="orders">Đơn hàng</SelectItem>
            <SelectItem value="tickets">Vé</SelectItem>
          </SelectContent>
        </Select>

        <Select value={chartType} onValueChange={setChartType}>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Chọn loại biểu đồ" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="bar">Cột</SelectItem>
            <SelectItem value="line">Đường</SelectItem>
            <SelectItem value="pie">Tròn</SelectItem>
          </SelectContent>
        </Select>

        <Select value={statType} onValueChange={setStatType}>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Chọn loại thống kê" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="monthly">Theo tháng</SelectItem>
            <SelectItem value="quarterly">Theo quý</SelectItem>
            <SelectItem value="yearly">Theo năm</SelectItem>
          </SelectContent>
        </Select>

        {/* chỉ hiện khi orders + pie */}
        {activeTab === "orders" && chartType === "pie" && (
          <Select value={pieMetric} onValueChange={setPieMetric}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Chọn số liệu" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="orders">Số đơn</SelectItem>
              <SelectItem value="revenue">Doanh thu</SelectItem>
            </SelectContent>
          </Select>
        )}
      </div>

      <Card>
        <CardContent className="h-[400px]">
          <ResponsiveContainer width="100%" height="100%">
            {renderChart()}
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  )
}

export default Dashboard

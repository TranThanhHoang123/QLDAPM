import { useSearchParams, Link } from "react-router-dom"
import { Layout } from "../layout"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

export default function PaymentResult() {
  const [searchParams] = useSearchParams()
  const orderId = searchParams.get("order_id")
  const status = searchParams.get("status")

  const getMessage = () => {
    switch (status) {
      case "OrderStatus.PAID":
      case "PAID":
        return {
          title: "✅ Thanh toán thành công",
          desc: `Đơn hàng #${orderId} đã được thanh toán.`,
          color: "text-green-600",
        }
      case "OrderStatus.FAILED":
      case "FAILED":
        return {
          title: "❌ Thanh toán thất bại",
          desc: `Đơn hàng #${orderId} thanh toán thất bại.`,
          color: "text-red-600",
        }
      case "OrderStatus.CANCELLED":
      case "CANCELLED":
        return {
          title: "⚠️ Thanh toán bị hủy",
          desc: `Đơn hàng #${orderId} đã bị hủy hoặc hết hạn.`,
          color: "text-yellow-600",
        }
      default:
        return {
          title: "ℹ️ Không xác định",
          desc: "Không tìm thấy thông tin thanh toán.",
          color: "text-gray-600",
        }
    }
  }

  const { title, desc, color } = getMessage()

  return (
    <Layout>
      <div className="max-w-md mx-auto py-12">
        <Card>
          <CardContent className="p-6 text-center space-y-6">
            <h1 className={`text-2xl font-bold ${color}`}>{title}</h1>
            <p className="text-gray-700">{desc}</p>
            {orderId && (
              <Link to={`/orders/${orderId}`}>
                <Button className="bg-blue-600 text-white">
                  Xem chi tiết đơn hàng
                </Button>
              </Link>
            )}
          </CardContent>
        </Card>
      </div>
    </Layout>
  )
}

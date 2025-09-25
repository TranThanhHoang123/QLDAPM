import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import orderService from "../../services/orderService"
import { Layout } from "../layout"
import { Card, CardContent } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"

export default function OrderDetail() {
  const { id } = useParams()
  const [order, setOrder] = useState(null)

  useEffect(() => {
    async function fetchOrder() {
      try {
        const res = await orderService.getOrderDetail(id)
        setOrder(res.data)
      } catch (err) {
        console.error("Lỗi khi lấy chi tiết đơn hàng:", err)
      }
    }
    fetchOrder()
  }, [id])

  if (!order) {
    return (
      <Layout>
        <div className="text-center py-12">Đang tải đơn hàng...</div>
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="max-w-3xl mx-auto py-12 px-4 space-y-6">
        <h1 className="text-2xl font-bold">Chi tiết đơn hàng #{order.id}</h1>

        <Card>
          <CardContent className="p-6 space-y-2">
            <p><strong>Trạng thái:</strong> {order.status}</p>
            <p><strong>Phương thức thanh toán:</strong> {order.payment_method}</p>
            <p><strong>Tổng tiền:</strong> {order.total_amount} VND</p>
            <p><strong>Người mua:</strong> {order.user.name} ({order.user.email})</p>
            <p><strong>Ngày tạo:</strong> {new Date(order.created_at).toLocaleString()}</p>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6 space-y-4">
            <h2 className="text-lg font-semibold">Danh sách vé</h2>
            <Separator />
            {order.items.map((item) => (
              <div
                key={item.id}
                className="flex items-center space-x-4 border-b pb-2"
              >
                <img
                  src={item.ticket.event.image}
                  alt={item.ticket.event.title}
                  className="w-16 h-16 object-cover rounded"
                />
                <div className="flex-1">
                  <p className="font-medium">{item.ticket.event.title}</p>
                  <p className="text-sm text-gray-600">
                    {item.ticket.type} – {item.ticket.price} VND
                  </p>
                  <p className="text-sm text-gray-500">
                    Trạng thái vé: {item.ticket.status}
                  </p>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </Layout>
  )
}

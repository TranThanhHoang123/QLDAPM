// src/pages/Checkout/index.jsx
import { useLocation, useNavigate } from "react-router-dom"
import { useState } from "react"
import { Layout } from "../layout"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Label } from "@/components/ui/label"
import toast from "react-hot-toast"
import orderService from "../../services/orderService"

export default function Checkout() {
  const location = useLocation()
  const navigate = useNavigate()

  // nhận dữ liệu từ navigate
  const { items = [] } = location.state || {}

  const [paymentMethod, setPaymentMethod] = useState("MOMO")

  const handleSubmit = async () => {
    if (!items.length) {
      toast.error("Giỏ hàng trống ❌")
      return
    }

    const payload = {
      payment_method: paymentMethod,
      items,
    }

    try {
      toast.success(`Đang xử lý thanh toán với ${paymentMethod} ✅`)

      const res = await orderService.createOrder(payload)

      // response có payment_url
      const { payment_url } = res.data
      if (payment_url) {
        // chuyển thẳng đến cổng thanh toán
        window.location.href = payment_url
      } else {
        toast.error("Không nhận được đường dẫn thanh toán ❌")
      }
    } catch (err) {
      console.error("Thanh toán lỗi:", err)
      toast.error("Thanh toán thất bại ❌")
    }
  }

  return (
    <Layout>
      <div className="max-w-3xl mx-auto px-4 py-12">
        <h1 className="text-2xl font-bold mb-6">Thanh toán</h1>

        {/* Danh sách vé */}
        <Card className="mb-6">
          <CardContent className="p-6 space-y-4">
            <h2 className="text-lg font-semibold">Vé của bạn</h2>
            {items.map((item, idx) => (
              <div
                key={idx}
                className="flex justify-between border-b py-2 text-sm"
              >
                <span>
                  Event #{item.event_id} – {item.ticket_type}
                </span>
                <span>x {item.quantity}</span>
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Phương thức thanh toán */}
        <Card className="mb-6">
          <CardContent className="p-6 space-y-4">
            <h2 className="text-lg font-semibold">Chọn phương thức thanh toán</h2>
            <RadioGroup
              value={paymentMethod}
              onValueChange={setPaymentMethod}
              className="space-y-2"
            >
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="MOMO" id="momo" />
                <Label htmlFor="momo">MOMO</Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="VNPAY" id="vnpay" />
                <Label htmlFor="vnpay">VNPAY</Label>
              </div>
            </RadioGroup>
          </CardContent>
        </Card>

        {/* Submit */}
        <Button
          className="w-full bg-blue-600 text-white"
          onClick={handleSubmit}
        >
          Thanh toán ngay
        </Button>
      </div>
    </Layout>
  )
}

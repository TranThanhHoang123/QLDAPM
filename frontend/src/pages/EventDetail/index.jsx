import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import eventService from "../../services/eventService"
import { Layout } from "../layout"
import { Badge } from "../../components/ui/badge"
import { Card, CardContent } from "../../components/ui/card"
import { Button } from "../../components/ui/button"
import cartService from "../../services/cartService"
import toast from "react-hot-toast"
import { useNavigate } from "react-router-dom"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "../../components/ui/dialog"
import { Input } from "../../components/ui/input"
import { Label } from "../../components/ui/label"
import { useCart } from "../../contexts/CartContext"
export default function EventDetail() {
  const navigate = useNavigate()
  const { id } = useParams()
  const [event, setEvent] = useState(null)
  const [loading, setLoading] = useState(false)
  const [openDialog, setOpenDialog] = useState(false)

  // state cho form đặt vé
  const [ticketType, setTicketType] = useState("STANDARD")
  const [quantity, setQuantity] = useState(1)
  const { setCartData } = useCart()
  useEffect(() => {
    async function fetchEvent() {
      try {
        setLoading(true)
        const res = await eventService.getDetail(id)
        setEvent(res.data)
      } catch (err) {
        console.error("Error fetching event detail:", err)
      } finally {
        setLoading(false)
      }
    }
    fetchEvent()
  }, [id])


  const handleAddToCart = async () => {
    try {
      const available = event.available_ticket_counts?.[ticketType] || 0
      if (available === 0) {
        toast.error("Loại vé này đã hết ❌")
        return
      }
      if (quantity > available) {
        toast.error(`Chỉ còn ${available} vé loại ${ticketType}`)
        return
      }

      const payload = {
        event_id: event.id,
        ticket_type: ticketType,
        quantity,
      }

      const res = await cartService.addTicket(payload)
      console.log("Đã thêm vào giỏ:", res.data)

      // cập nhật giỏ
      setCartData((prev) => {
        if (!prev || !prev.items) {
          return { items: [res.data] }
        }

        const exists = prev.items.find(
          (i) => i.id === res.data.id || (
            i.event.id === payload.event_id &&
            i.ticket_type === payload.ticket_type
          )
        )

        if (exists) {
          return {
            ...prev,
            items: prev.items.map((i) =>
              i.id === exists.id
                ? { ...i, quantity: i.quantity + payload.quantity }
                : i
            ),
          }
        }

        return {
          ...prev,
          items: [...prev.items, res.data],
        }
      })

      setOpenDialog(false)
      toast.success("Thêm vào giỏ hàng thành công ✅")
    } catch (err) {
      console.error("Lỗi khi thêm vào giỏ:", err)
      toast.error("Không thể thêm vào giỏ hàng ❌")
    }
  }


  const handleCheckout = () => {
    if (!event?.available_ticket_counts?.[ticketType]) {
      toast.error("Loại vé này đã hết ❌")
      return
    }

    if (quantity <= 0) {
      toast.error("Số lượng vé không hợp lệ ❌")
      return
    }
    navigate("/checkout", {
      state: {
        items: [
          {
            event_id: event.id,
            ticket_type: ticketType,
            quantity,
          },
        ],
      },
    })
  }


  if (loading) {
    return (
      <Layout>
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-4 border-gray-300 border-t-transparent"></div>
        </div>
      </Layout>
    )
  }

  if (!event) {
    return (
      <Layout>
        <div className="text-center py-20 text-gray-500">Không tìm thấy sự kiện</div>
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="max-w-4xl mx-auto px-4 py-12">
        <Card className="overflow-hidden">
          <img
            src={event.image || "/placeholder.svg"}
            alt={event.title}
            className="w-full h-96 object-cover"
          />
          <CardContent className="p-6">
            <Badge className="mb-4">{event.category?.name || "Uncategorized"}</Badge>
            <h1 className="text-3xl font-bold text-gray-900 mb-4">{event.title}</h1>
            <p className="text-gray-700 mb-4">{event.description}</p>

            {/* Vé */}
            <div className="space-y-2 mb-6">
              <h2 className="text-lg font-semibold mb-2">Vé</h2>
              {Object.entries(event.available_ticket_counts).map(([type, info]) => (
  <p
    key={type}
    className={info.count > 0 ? "text-green-600" : "text-red-500"}
  >
    {type}: {info.count > 0
      ? `${info.count} vé còn lại - ${info.price.toLocaleString()} VND`
      : "Hết vé"}
  </p>
))}
            </div>

            {/* Nút đặt vé */}
            <Button className="bg-blue-600 text-white" onClick={() => setOpenDialog(true)}>
              Đặt vé
            </Button>
            <Dialog open={openDialog} onOpenChange={setOpenDialog}>
              <DialogContent className="max-w-md bg-white shadow-lg rounded-lg">
                <DialogHeader>
                  <DialogTitle>Chọn vé</DialogTitle>
                </DialogHeader>

                <div className="space-y-4 py-4">
                  <div className="space-y-2">
                    <Label htmlFor="ticketType">Loại vé</Label>
                    <select
                      id="ticketType"
                      value={ticketType}
                      onChange={(e) => setTicketType(e.target.value)}
                      className="w-full border rounded px-3 py-2"
                    >
                      <option value="">-- Chọn loại vé --</option>
                      {Object.entries(event.available_ticket_counts).map(([type, info]) => (
  <option key={type} value={type} disabled={info.count === 0}>
    {type} ({info.count} còn lại - {info.price.toLocaleString()} VND)
  </option>
))}
                    </select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="quantity">Số lượng</Label>
                    <Input
                      id="quantity"
                      type="number"
                      min={1}
                      value={quantity}
                      onChange={(e) => setQuantity(Number(e.target.value))}
                    />
                  </div>
                </div>

                <DialogFooter className="flex justify-between">
                  <Button variant="ghost" onClick={() => setOpenDialog(false)}>
                    Hủy
                  </Button>
                  <div className="flex gap-2">
                    <Button variant="outline" onClick={handleAddToCart}>
                      Thêm vào giỏ
                    </Button>
                    <Button className="bg-blue-600 text-white" onClick={handleCheckout}>
                      Thanh toán ngay
                    </Button>
                  </div>
                </DialogFooter>
              </DialogContent>
            </Dialog>
          </CardContent>
        </Card>
      </div>
    </Layout>
  )
}

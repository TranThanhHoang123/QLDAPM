import { useEffect, useState } from "react"
import { Eye } from "lucide-react"
import toast from "react-hot-toast"
import { useNavigate } from "react-router-dom"
import orderService from "../../../services/orderService"

function AdminOrder() {
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)
  const [page, setPage] = useState(1)
  const [pages, setPages] = useState(1)

  // bộ lọc
  const [userId, setUserId] = useState("")
  const [status, setStatus] = useState("")
  const [paymentMethod, setPaymentMethod] = useState("")

  const navigate = useNavigate()

  useEffect(() => {
    async function fetchOrders() {
      setLoading(true)
      try {
        const res = await orderService.getManagerOrderList({
          page,
          page_size: 5,
          user_id: userId || undefined,
          status: status || undefined,
          payment_method: paymentMethod || undefined,
        })
        setOrders(res.data.items || [])
        setPages(res.data.pages || 1)
      } catch (err) {
        console.error("Failed to fetch orders", err)
        toast.error("Load order thất bại")
      } finally {
        setLoading(false)
      }
    }
    fetchOrders()
  }, [page, userId, status, paymentMethod])

  if (loading) return <p className="p-4">Loading...</p>

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Order Management</h1>

      {/* Bộ lọc */}
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-4">
        <input
          type="text"
          placeholder="User ID"
          className="border p-2 rounded"
          value={userId}
          onChange={(e) => {
            setUserId(e.target.value)
            setPage(1)
          }}
        />
        <select
          className="border p-2 rounded"
          value={status}
          onChange={(e) => {
            setStatus(e.target.value)
            setPage(1)
          }}
        >
          <option value="">-- Status --</option>
          <option value="PAID">PAID</option>
          <option value="CANCELLED">CANCELLED</option>
          <option value="PENDING">PENDING</option>
        </select>
        <select
          className="border p-2 rounded"
          value={paymentMethod}
          onChange={(e) => {
            setPaymentMethod(e.target.value)
            setPage(1)
          }}
        >
          <option value="">-- Payment --</option>
          <option value="MOMO">MOMO</option>
          <option value="VNPAY">VNPAY</option>
          <option value="CASH">CASH</option>
        </select>
      </div>

      {/* Bảng */}
      {orders.length === 0 ? (
        <p>No orders found.</p>
      ) : (
        <table className="w-full border-collapse border border-gray-200">
          <thead>
            <tr className="bg-gray-100">
              <th className="border p-2">ID</th>
              <th className="border p-2">Payment</th>
              <th className="border p-2">Status</th>
              <th className="border p-2">Total Amount</th>
              <th className="border p-2">Action</th>
            </tr>
          </thead>
          <tbody>
            {orders.map((o) => (
              <tr key={o.id} className="text-center">
                <td className="border p-2">{o.id}</td>
                <td className="border p-2">{o.payment_method}</td>
                <td className="border p-2">{o.status}</td>
                <td className="border p-2">{o.total_amount}</td>
                <td className="border p-2">
                  <button
                    onClick={() => navigate(`/admin/order/detail/${o.id}`)}
                    className="flex items-center gap-1 text-blue-600 hover:underline justify-center"
                  >
                    <Eye className="h-4 w-4" /> View
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {/* Pagination */}
      <div className="flex justify-center items-center gap-4 mt-4">
        <button
          disabled={page <= 1}
          onClick={() => setPage((p) => Math.max(1, p - 1))}
          className="px-3 py-1 border rounded disabled:opacity-50"
        >
          Prev
        </button>
        <span>
          Page {page} / {pages}
        </span>
        <button
          disabled={page >= pages}
          onClick={() => setPage((p) => Math.min(pages, p + 1))}
          className="px-3 py-1 border rounded disabled:opacity-50"
        >
          Next
        </button>
      </div>
    </div>
  )
}

export default AdminOrder

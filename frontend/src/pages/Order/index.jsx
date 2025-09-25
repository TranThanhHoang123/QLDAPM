import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import orderService from "../../services/orderService"
import {Layout} from "../layout"

function Order() {
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)
  const [page, setPage] = useState(1)
  const [pages, setPages] = useState(1)
  const [status, setStatus] = useState("")
  const [paymentMethod, setPaymentMethod] = useState("")

  useEffect(() => {
    async function fetchOrders() {
      setLoading(true)
      try {
        const res = await orderService.getOrderList({
          page,
          page_size: 5,
          status: status || undefined,
          payment_method: paymentMethod || undefined,
        })
        setOrders(res.data.items || [])
        setPages(res.data.pages || 1)
      } catch (err) {
        console.error("Failed to fetch orders", err)
      } finally {
        setLoading(false)
      }
    }
    fetchOrders()
  }, [page, status, paymentMethod])

  if (loading) return <Layout><p className="p-4">Loading...</p></Layout>

  return (
    <Layout>
      <div className="p-6 max-w-5xl mx-auto">
        <h1 className="text-2xl font-bold mb-4">Your Orders</h1>

        {/* Bộ lọc */}
        <div className="flex gap-4 mb-4">
          <select
            className="border p-2 rounded"
            value={status}
            onChange={(e) => {
              setStatus(e.target.value)
              setPage(1)
            }}
          >
            <option value="">All Status</option>
            <option value="PAID">Paid</option>
            <option value="FAILED">Failed</option>
            <option value="CANCELLED">Cancelled</option>
          </select>

          <select
            className="border p-2 rounded"
            value={paymentMethod}
            onChange={(e) => {
              setPaymentMethod(e.target.value)
              setPage(1)
            }}
          >
            <option value="">All Payment</option>
            <option value="MOMO">MOMO</option>
            <option value="VNPAY">VNPAY</option>
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
                <th className="border p-2">Payment Method</th>
                <th className="border p-2">Status</th>
                <th className="border p-2">Total</th>
                <th className="border p-2">Actions</th>
              </tr>
            </thead>
            <tbody>
              {orders.map((order) => (
                <tr key={order.id} className="text-center">
                  <td className="border p-2">{order.id}</td>
                  <td className="border p-2">{order.payment_method}</td>
                  <td
                    className={`border p-2 font-medium ${
                      order.status === "PAID"
                        ? "text-green-600"
                        : order.status === "FAILED"
                        ? "text-red-600"
                        : "text-gray-600"
                    }`}
                  >
                    {order.status}
                  </td>
                  <td className="border p-2">
                    {Number(order.total_amount).toLocaleString()} VND
                  </td>
                  <td className="border p-2">
                    <Link
                      to={`/orders/${order.id}`}
                      className="text-blue-600 hover:underline"
                    >
                      View
                    </Link>
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
    </Layout>
  )
}

export default Order

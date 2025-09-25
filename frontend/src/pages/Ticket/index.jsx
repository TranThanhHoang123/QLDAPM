// src/pages/ticket/index.jsx
import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import ticketService from "../../services/ticketService"
import { Layout } from "../layout"
import { Eye } from "lucide-react"

function Ticket() {
  const [tickets, setTickets] = useState([])
  const [loading, setLoading] = useState(true)
  const [page, setPage] = useState(1)
  const [pages, setPages] = useState(1)
  const [status, setStatus] = useState("")
  const [type, setType] = useState("")
  const navigate = useNavigate()

  useEffect(() => {
    async function fetchTickets() {
      setLoading(true)
      try {
        const res = await ticketService.getTicketList({
          page,
          page_size: 5,
          status: status || undefined,
          type: type || undefined,
        })
        setTickets(res.data.items || [])
        setPages(res.data.pages || 1)
      } catch (err) {
        console.error("Failed to fetch tickets", err)
      } finally {
        setLoading(false)
      }
    }
    fetchTickets()
  }, [page, status, type])

  if (loading) return <Layout><p className="p-4">Loading...</p></Layout>

  return (
    <Layout>
      <div className="p-6 max-w-5xl mx-auto">
        <h1 className="text-2xl font-bold mb-4">Your Tickets</h1>

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
            <option value="AVAILABLE">Available</option>
            <option value="SOLD">Sold</option>
            <option value="RESERVED">Reserved</option>
            <option value="CANCELLED">Cancelled</option>
          </select>

          <select
            className="border p-2 rounded"
            value={type}
            onChange={(e) => {
              setType(e.target.value)
              setPage(1)
            }}
          >
            <option value="">All Type</option>
            <option value="VIP">VIP</option>
            <option value="STANDARD">Standard</option>
          </select>
        </div>

        {/* Bảng */}
        {tickets.length === 0 ? (
          <p>No tickets found.</p>
        ) : (
          <table className="w-full border-collapse border border-gray-200">
            <thead>
              <tr className="bg-gray-100">
                <th className="border p-2">ID</th>
                <th className="border p-2">Event</th>
                <th className="border p-2">Type</th>
                <th className="border p-2">Price</th>
                <th className="border p-2">Status</th>
                <th className="border p-2">Action</th>
              </tr>
            </thead>
            <tbody>
              {tickets.map((ticket) => (
                <tr key={ticket.id} className="text-center">
                  <td className="border p-2">{ticket.id}</td>
                  <td className="border p-2">{ticket.event?.title}</td>
                  <td className="border p-2">{ticket.type}</td>
                  <td className="border p-2">
                    {Number(ticket.price).toLocaleString()} VND
                  </td>
                  <td
                    className={`border p-2 font-medium ${
                      ticket.status === "AVAILABLE"
                        ? "text-green-600"
                        : ticket.status === "SOLD"
                        ? "text-red-600"
                        : "text-gray-600"
                    }`}
                  >
                    {ticket.status}
                  </td>
                  <td className="border p-2">
                    <button
                      onClick={() => navigate(`/ticket/${ticket.id}`)}
                      className="flex items-center justify-center gap-1 text-blue-600 hover:underline"
                    >
                      <Eye className="h-4 w-4" />
                      View
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
    </Layout>
  )
}

export default Ticket

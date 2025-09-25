// src/pages/ticket/TicketDetail.jsx
import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import ticketService from "../../services/ticketService"
import {Layout} from "../layout"

function TicketDetail() {
  const { id } = useParams()
  const [ticket, setTicket] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchTicket() {
      try {
        const res = await ticketService.getTicketDetail(id)
        setTicket(res.data)
      } catch (err) {
        console.error("Failed to fetch ticket", err)
      } finally {
        setLoading(false)
      }
    }
    fetchTicket()
  }, [id])

  if (loading) {
    return (
      <Layout>
        <p className="p-4">Loading ticket details...</p>
      </Layout>
    )
  }

  if (!ticket) {
    return (
      <Layout>
        <p className="p-4 text-red-600">Ticket not found</p>
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="p-6 max-w-3xl mx-auto">
        <h1 className="text-2xl font-bold mb-4">Ticket Detail</h1>

        {/* Event Info */}
        <div className="border rounded-lg p-4 mb-4 shadow-sm">
          <h2 className="text-xl font-semibold mb-2">{ticket.event.title}</h2>
          <img
            src={ticket.event.image}
            alt={ticket.event.title}
            className="w-full h-48 object-cover rounded mb-2"
          />
          <p className="text-gray-600">
            <strong>Category:</strong> {ticket.event.category.name}
          </p>
          <p className="text-gray-600">
            <strong>Location:</strong> {ticket.event.location}
          </p>
          <p className="text-gray-600">
            <strong>Time:</strong> {ticket.event.start_time} → {ticket.event.end_time}
          </p>
        </div>

        {/* Ticket Info */}
        <div className="border rounded-lg p-4 mb-4 shadow-sm">
          <h2 className="text-xl font-semibold mb-2">Ticket Info</h2>
          <p>
            <strong>ID:</strong> {ticket.id}
          </p>
          <p>
            <strong>Type:</strong> {ticket.type}
          </p>
          <p>
            <strong>Status:</strong>{" "}
            <span
              className={`font-medium ${
                ticket.status === "AVAILABLE"
                  ? "text-green-600"
                  : ticket.status === "SOLD"
                  ? "text-red-600"
                  : "text-gray-600"
              }`}
            >
              {ticket.status}
            </span>
          </p>
          <p>
            <strong>Price:</strong> {Number(ticket.price).toLocaleString()} VND
          </p>
        </div>

        {/* User Info */}
        {ticket.user && (
          <div className="border rounded-lg p-4 shadow-sm">
            <h2 className="text-xl font-semibold mb-2">User Info</h2>
            <p>
              <strong>Name:</strong> {ticket.user.name}
            </p>
            <p>
              <strong>Email:</strong> {ticket.user.email}
            </p>
            <p>
              <strong>Phone:</strong> {ticket.user.phone_number}
            </p>
            <p>
              <strong>Username:</strong> {ticket.user.username}
            </p>
          </div>
        )}
      </div>
    </Layout>
  )
}

export default TicketDetail

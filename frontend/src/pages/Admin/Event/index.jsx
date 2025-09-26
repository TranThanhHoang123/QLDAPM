import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { Eye, Trash } from "lucide-react"
import eventService from "../../../services/eventService"
import categoryService from "../../../services/categoryService"
import ticketService from "../../../services/ticketService"
import toast from "react-hot-toast"

function AdminEvent() {
  const [events, setEvents] = useState([])
  const [loading, setLoading] = useState(true)
  const [page, setPage] = useState(1)
  const [pages, setPages] = useState(1)
  const [title, setTitle] = useState("")
  const [location, setLocation] = useState("")
  const [category, setCategory] = useState("")
  const [categories, setCategories] = useState([])
  const [startTime, setStartTime] = useState("")
  const [endTime, setEndTime] = useState("")
  const [selectedEvent, setSelectedEvent] = useState(null)
  const [type, setType] = useState("")
  const [price, setPrice] = useState("")
  const [quantity, setQuantity] = useState("")
  const navigate = useNavigate()

  // Fetch categories
  useEffect(() => {
    async function fetchCategories() {
      try {
        const res = await categoryService.getList()
        setCategories(res.data.items || [])
      } catch (err) {
        console.error("Failed to fetch categories", err)
      }
    }
    fetchCategories()
  }, [])

  useEffect(() => {
    async function fetchEvents() {
      setLoading(true)
      try {
        const res = await eventService.getList({
          title: title || undefined,
          location: location || undefined,
          category_id: category || undefined,
          start_time: startTime || undefined,
          end_time: endTime || undefined,
          page,
          page_size: 5,
        })
        setEvents(res.data.items || [])
        setPages(res.data.pages || 1)
      } catch (err) {
        console.error("Failed to fetch events", err)
      } finally {
        setLoading(false)
      }
    }
    fetchEvents()
  }, [page, title, location, category, startTime, endTime])

  if (loading) return <p className="p-4">Loading...</p>

  const handleDelete = async (id) => {
    if (!window.confirm("Bạn có chắc chắn muốn xóa sự kiện này?")) return
    try {
      await eventService.remove(id)
      setEvents((prev) => prev.filter((e) => e.id !== id))
    } catch (err) {
      console.error("Delete failed", err)
      toast.error("Xóa thất bại")
    }
  }

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Events</h1>

      {/* Bộ lọc */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 mb-4">
        <input
          type="text"
          placeholder="Title"
          className="border p-2 rounded"
          value={title}
          onChange={(e) => {
            setTitle(e.target.value)
            setPage(1)
          }}
        />
        <input
          type="text"
          placeholder="Location"
          className="border p-2 rounded"
          value={location}
          onChange={(e) => {
            setLocation(e.target.value)
            setPage(1)
          }}
        />
        <select
          className="border p-2 rounded"
          value={category}
          onChange={(e) => {
            setCategory(e.target.value)
            setPage(1)
          }}
        >
          <option value="">All Categories</option>
          {categories.map((c) => (
            <option key={c.id} value={c.id}>
              {c.name}
            </option>
          ))}
        </select>
        <input
          type="datetime-local"
          className="border p-2 rounded"
          value={startTime}
          onChange={(e) => {
            setStartTime(e.target.value)
            setPage(1)
          }}
        />
        <input
          type="datetime-local"
          className="border p-2 rounded"
          value={endTime}
          onChange={(e) => {
            setEndTime(e.target.value)
            setPage(1)
          }}
        />
      </div>
      {/* action */}
      <button
        onClick={() => navigate("/admin/event/new")}
        className="mb-4 px-4 py-2 bg-green-600 text-white rounded"
      >
        + New Event
      </button>

      {/* Bảng */}
      {events.length === 0 ? (
        <p>No events found.</p>
      ) : (
        <table className="w-full border-collapse border border-gray-200">
          <thead>
            <tr className="bg-gray-100">
              <th className="border p-2">ID</th>
              <th className="border p-2">Title</th>
              <th className="border p-2">Location</th>
              <th className="border p-2">Start Time</th>
              <th className="border p-2">End Time</th>
              <th className="border p-2">Action</th>
              <th className="border p-2">Tickets</th>
            </tr>
          </thead>
          <tbody>
            {events.map((event) => (
              <tr key={event.id} className="text-center">
                <td className="border p-2">{event.id}</td>
                <td className="border p-2">{event.title}</td>
                <td className="border p-2">{event.location}</td>
                <td className="border p-2">
                  {new Date(event.start_time).toLocaleString()}
                </td>
                <td className="border p-2">
                  {new Date(event.end_time).toLocaleString()}
                </td>
                <td className="border p-2 flex justify-center gap-2">
                  <button
                    onClick={() => navigate(`/admin/event/detail/${event.id}`)}
                    className="flex items-center gap-1 text-blue-600 hover:underline"
                  >
                    <Eye className="h-4 w-4" /> View
                  </button>
                  <button
                    onClick={() => handleDelete(event.id)}
                    className="flex items-center gap-1 text-red-600 hover:underline"
                  >
                    <Trash className="h-4 w-4" /> Delete
                  </button>
                  <button
                    onClick={() => setSelectedEvent(event)}
                    className="flex items-center gap-1 text-green-600 hover:underline"
                  >
                    + Ticket
                  </button>
                </td>
                <td className="border p-2">
                  VIP: {event.available_ticket_counts?.VIP?.count || 0} vé - 
                      {event.available_ticket_counts?.VIP?.price || 0}đ
                  <br />
                  STANDARD: {event.available_ticket_counts?.STANDARD?.count || 0} vé - 
                            {event.available_ticket_counts?.STANDARD?.price || 0}đ
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
      {selectedEvent && (
  <div className="fixed inset-0 bg-black/50 flex items-center justify-center">
    <div className="bg-white p-6 rounded shadow w-96">
      <h2 className="text-lg font-bold mb-4">Add Ticket for {selectedEvent.title}</h2>
      <form
        onSubmit={async (e) => {
          e.preventDefault()
          try {
            await ticketService.createTicket({
              event_id: selectedEvent.id,
              type,
              price,
              quantity,
            })
            toast.success("Ticket added")
            setSelectedEvent(null)
            setType("")
            setPrice("")
            setQuantity("")
          } catch (err) {
            console.error(err)
            toast.error("Failed to add ticket")
          }
        }}
        className="flex flex-col gap-3"
      >
        <select
          value={type}
          onChange={(e) => setType(e.target.value)}
          className="border p-2 rounded"
        >
          <option value="">Select Type</option>
          <option value="VIP">VIP</option>
          <option value="STANDARD">STANDARD</option>
        </select>
        <input
          type="number"
          placeholder="Price"
          className="border p-2 rounded"
          value={price}
          onChange={(e) => setPrice(e.target.value)}
        />
        <input
          type="number"
          placeholder="Quantity"
          className="border p-2 rounded"
          value={quantity}
          onChange={(e) => setQuantity(e.target.value)}
        />
        <div className="flex justify-end gap-2">
          <button
            type="button"
            onClick={() => setSelectedEvent(null)}
            className="px-4 py-2 border rounded"
          >
            Cancel
          </button>
          <button
            type="submit"
            className="px-4 py-2 bg-blue-600 text-white rounded"
          >
            Save
          </button>
        </div>
      </form>
    </div>
  </div>
)}
    </div>
  )
}

export default AdminEvent

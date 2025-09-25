import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import eventService from "../../../services/eventService"
import toast from "react-hot-toast"
import EventForm from "./EventForm"
function EventDetail() {
  const { id } = useParams()
  const [event, setEvent] = useState(null)
  const [loading, setLoading] = useState(true)
  const [editing, setEditing] = useState(false)
  const [form, setForm] = useState({
    title: "",
    description: "",
    location: "",
    start_time: "",
    end_time: "",
    category_id: "",
    image: null,
  })

  // format từ API → input
  const toInputDateTime = (dt) => {
    if (!dt) return ""
    const d = new Date(dt)
    const pad = (n) => String(n).padStart(2, "0")
    return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`
  }

  useEffect(() => {
    async function fetchEvent() {
      try {
        const res = await eventService.getDetail(id)
        setEvent(res.data)
        setForm({
          title: res.data.title,
          description: res.data.description,
          location: res.data.location,
          start_time: toInputDateTime(res.data.start_time),
          end_time: toInputDateTime(res.data.end_time),
          category_id: res.data.category_id,
          image: null,
        })
      } catch (err) {
        console.error("Failed to fetch event", err)
      } finally {
        setLoading(false)
      }
    }
    fetchEvent()
  }, [id])

  if (loading) return <p className="p-4">Loading...</p>
  if (!event) return <p className="p-4">Event not found</p>

  return (
    <EventForm
      initialData={event}
      onSubmit={(data) => eventService.update(id, data)}
    />
  )
}

export default EventDetail

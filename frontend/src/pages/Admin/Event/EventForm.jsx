import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import toast from "react-hot-toast"
import categoryService from "../../../services/categoryService"

function EventForm({ initialData, onSubmit }) {
    const [form, setForm] = useState(initialData)
    const [categories, setCategories] = useState([])
    const navigate = useNavigate()

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

    const handleChange = (e) => {
        const { name, value, files } = e.target
        setForm({ ...form, [name]: files ? files[0] : value })
    }

    function formatDateTimeLocal(value) {
        if (!value) return null
        const date = new Date(value)
        // format thành "YYYY-MM-DD HH:mm:ss"
        const pad = (n) => String(n).padStart(2, "0")
        return (
            date.getFullYear() +
            "-" +
            pad(date.getMonth() + 1) +
            "-" +
            pad(date.getDate()) +
            " " +
            pad(date.getHours()) +
            ":" +
            pad(date.getMinutes()) +
            ":" +
            pad(date.getSeconds())
        )
    }

    const handleSubmit = async (e) => {
  e.preventDefault()
  try {
    let payload

    if (initialData.id) {
      // === Edit mode ===
      const changedFields = {}
      for (const key in form) {
        if (form[key] !== initialData[key] && form[key] !== null) {
          changedFields[key] = form[key]
        }
      }

      if (changedFields.start_time) {
        changedFields.start_time = formatDateTimeLocal(form.start_time)
      }
      if (changedFields.end_time) {
        changedFields.end_time = formatDateTimeLocal(form.end_time)
      }

      if (changedFields.image) {
        payload = new FormData()
        Object.entries(changedFields).forEach(([key, value]) => {
          payload.append(key, value)
        })
      } else {
        payload = changedFields
      }
    } else {
      // === Create mode ===
      payload = { ...form }
      payload.start_time = formatDateTimeLocal(form.start_time)
      payload.end_time = formatDateTimeLocal(form.end_time)

      if (form.image) {
        const fd = new FormData()
        Object.entries(payload).forEach(([key, value]) => {
          fd.append(key, value)
        })
        payload = fd
      }
    }

    // 🔥 log payload trước khi gửi
    if (payload instanceof FormData) {
      for (let [key, value] of payload.entries()) {
        console.log("FormData field:", key, value)
      }
    } else {
      console.log("JSON payload:", payload)
    }

    await onSubmit(payload)
    toast.success("Lưu thành công!")
    navigate("/admin/event")
  } catch (err) {
    console.error("Save failed", err)
    toast.error("Lưu thất bại")
  }
}


    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            <input
                type="text"
                name="title"
                value={form.title}
                onChange={handleChange}
                className="w-full border p-2 rounded"
                placeholder="Title"
            />
            <textarea
                name="description"
                value={form.description}
                onChange={handleChange}
                className="w-full border p-2 rounded"
                placeholder="Description"
            />
            <input
                type="text"
                name="location"
                value={form.location}
                onChange={handleChange}
                className="w-full border p-2 rounded"
                placeholder="Location"
            />
            <input
                type="datetime-local"
                name="start_time"
                value={form.start_time}
                onChange={handleChange}
                className="w-full border p-2 rounded"
            />
            <input
                type="datetime-local"
                name="end_time"
                value={form.end_time}
                onChange={handleChange}
                className="w-full border p-2 rounded"
            />
            <select
                name="category_id"
                value={form.category_id}
                onChange={handleChange}
                className="w-full border p-2 rounded"
            >
                <option value="">Select Category</option>
                {categories.map((c) => (
                    <option key={c.id} value={c.id}>
                        {c.name}
                    </option>
                ))}
            </select>
            <input
                type="file"
                name="image"
                accept="image/*"
                onChange={handleChange}
                className="w-full"
            />
            <div className="flex gap-4">
                <button
                    type="submit"
                    className="px-4 py-2 bg-green-600 text-white rounded"
                >
                    Save
                </button>
                <button
                    type="button"
                    onClick={() => navigate("/admin/event")}
                    className="px-4 py-2 bg-gray-400 text-white rounded"
                >
                    Cancel
                </button>
            </div>
        </form>
    )
}

export default EventForm

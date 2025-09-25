import { useState } from "react"
import { useNavigate } from "react-router-dom"
import toast from "react-hot-toast"
import userService from "../../../services/userService"

function UserForm() {
  const navigate = useNavigate()
  const [form, setForm] = useState({
    username: "",
    name: "",
    email: "",
    phone_number: "",
    password: "",
  })

  const handleChange = (e) => {
    const { name, value } = e.target
    setForm({ ...form, [name]: value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      await userService.createManager(form)
      toast.success("Tạo manager thành công!")
      navigate("/admin/user")
    } catch (err) {
      console.error("Create manager failed", err)
      toast.error("Tạo thất bại")
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4 max-w-md mx-auto">
      <input
        type="text"
        name="username"
        placeholder="Username"
        value={form.username}
        onChange={handleChange}
        className="w-full border p-2 rounded"
      />
      <input
        type="text"
        name="name"
        placeholder="Name"
        value={form.name}
        onChange={handleChange}
        className="w-full border p-2 rounded"
      />
      <input
        type="email"
        name="email"
        placeholder="Email"
        value={form.email}
        onChange={handleChange}
        className="w-full border p-2 rounded"
      />
      <input
        type="text"
        name="phone_number"
        placeholder="Phone Number"
        value={form.phone_number}
        onChange={handleChange}
        className="w-full border p-2 rounded"
      />
      <input
        type="password"
        name="password"
        placeholder="Password"
        value={form.password}
        onChange={handleChange}
        className="w-full border p-2 rounded"
      />
      <div className="flex gap-4">
        <button type="submit" className="px-4 py-2 bg-green-600 text-white rounded">
          Save
        </button>
        <button
          type="button"
          onClick={() => navigate("/admin/user")}
          className="px-4 py-2 bg-gray-400 text-white rounded"
        >
          Cancel
        </button>
      </div>
    </form>
  )
}

export default UserForm

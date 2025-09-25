import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { Eye, Trash } from "lucide-react"
import toast from "react-hot-toast"
import userService from "../../../services/userService"

function AdminUser() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [page, setPage] = useState(1)
  const [pages, setPages] = useState(1)
  const [username, setUsername] = useState("")
  const [email, setEmail] = useState("")
  const navigate = useNavigate()

  useEffect(() => {
    async function fetchUsers() {
      setLoading(true)
      try {
        const res = await userService.getList({
          page,
          page_size: 5,
          username: username || undefined,
          email: email || undefined,
        })
        setUsers(res.data.items || [])
        setPages(res.data.pages || 1)
      } catch (err) {
        console.error("Failed to fetch users", err)
        toast.error("Load user thất bại")
      } finally {
        setLoading(false)
      }
    }
    fetchUsers()
  }, [page, username, email])

  if (loading) return <p className="p-4">Loading...</p>

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">User Management</h1>

      {/* Bộ lọc */}
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-4">
        <input
          type="text"
          placeholder="Username"
          className="border p-2 rounded"
          value={username}
          onChange={(e) => {
            setUsername(e.target.value)
            setPage(1)
          }}
        />
        <input
          type="text"
          placeholder="Email"
          className="border p-2 rounded"
          value={email}
          onChange={(e) => {
            setEmail(e.target.value)
            setPage(1)
          }}
        />
      </div>

      {/* Action */}
      <button
        onClick={() => navigate("/admin/user/new")}
        className="mb-4 px-4 py-2 bg-green-600 text-white rounded"
      >
        + New Manager
      </button>

      {/* Bảng */}
      {users.length === 0 ? (
        <p>No users found.</p>
      ) : (
        <table className="w-full border-collapse border border-gray-200">
          <thead>
            <tr className="bg-gray-100">
              <th className="border p-2">ID</th>
              <th className="border p-2">Username</th>
              <th className="border p-2">Name</th>
              <th className="border p-2">Email</th>
              <th className="border p-2">Phone</th>
              <th className="border p-2">Role</th>
              <th className="border p-2">Action</th>
            </tr>
          </thead>
          <tbody>
            {users.map((u) => (
              <tr key={u.id} className="text-center">
                <td className="border p-2">{u.id}</td>
                <td className="border p-2">{u.username}</td>
                <td className="border p-2">{u.name}</td>
                <td className="border p-2">{u.email}</td>
                <td className="border p-2">{u.phone_number}</td>
                <td className="border p-2">{u.role}</td>
                <td className="border p-2 flex justify-center gap-2">
                  <button
                    onClick={() => navigate(`/admin/user/detail/${u.id}`)}
                    className="flex items-center gap-1 text-blue-600 hover:underline"
                  >
                    <Eye className="h-4 w-4" /> View
                  </button>
                  <button
                    onClick={() => toast("Delete API chưa làm")}
                    className="flex items-center gap-1 text-red-600 hover:underline"
                  >
                    <Trash className="h-4 w-4" /> Delete
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

export default AdminUser

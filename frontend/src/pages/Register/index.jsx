import { useState } from "react"
import { User, Lock, Mail, Phone, Eye, EyeOff } from "lucide-react"
import { useNavigate } from "react-router-dom"
import userService from "../../services/userService"

function Register() {
  const navigate = useNavigate()
  const [form, setForm] = useState({
    username: "",
    password: "",
    name: "",
    email: "",
    phone_number: ""
  })
  const [loading, setLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState("")

  const handleChange = (e) => {
    const { name, value } = e.target
    setForm(prev => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError("")
    try {
      const res = await userService.register(
        form.username,
        form.password,
        form.name,
        form.email,
        form.phone_number
      )
      if (res.status === 200 || res.status === 201) {
        navigate("/login")
      } else {
        throw new Error("Status code: " + res.status)
      }
    } catch (err) {
      console.error("Register error:", err.response || err)
      setError(err.response?.data?.message || err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-gray-100 px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-xl p-8">
        <div className="flex flex-col items-center mb-6">
          <div className="flex items-center justify-center w-16 h-16 rounded-full bg-gray-200 text-gray-600 mb-4">
            <User className="w-8 h-8" />
          </div>
          <h2 className="text-2xl font-bold text-gray-800">Đăng ký</h2>
          <p className="text-gray-500 text-sm">Tạo tài khoản mới</p>
        </div>

        {error && (
          <div className="mb-4 p-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <InputField
            icon={<User size={18} className="text-gray-400 mr-2" />}
            name="name"
            placeholder="Họ và tên"
            value={form.name}
            onChange={handleChange}
          />
          <InputField
            icon={<User size={18} className="text-gray-400 mr-2" />}
            name="username"
            placeholder="Tên đăng nhập"
            value={form.username}
            onChange={handleChange}
          />
          <InputField
            icon={<Mail size={18} className="text-gray-400 mr-2" />}
            name="email"
            placeholder="Email"
            value={form.email}
            onChange={handleChange}
          />
          <InputField
            icon={<Phone size={18} className="text-gray-400 mr-2" />}
            name="phone_number"
            placeholder="Số điện thoại"
            value={form.phone_number}
            onChange={handleChange}
          />
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Mật khẩu</label>
            <div className="flex items-center px-3 py-2 border rounded-lg bg-gray-50 relative">
              <Lock className="text-gray-400 mr-2" size={18} />
              <input
                type={showPassword ? "text" : "password"}
                name="password"
                placeholder="Mật khẩu"
                value={form.password}
                onChange={handleChange}
                className="w-full bg-gray-50 outline-none pr-10"
                required
              />
              <div
                className="absolute right-3 top-2.5 text-gray-400 cursor-pointer"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
              </div>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 disabled:opacity-50 transition-colors"
          >
            {loading ? "Đang đăng ký..." : "Đăng ký"}
          </button>
        </form>

        <p className="text-center text-sm text-gray-500 mt-6">
          Bạn đã có tài khoản?{" "}
          <span
            className="text-indigo-600 cursor-pointer hover:underline"
            onClick={() => navigate("/login")}
          >
            Đăng nhập
          </span>
        </p>
      </div>
    </div>
  )
}

// Component con để tránh crash
function InputField({ icon, name, placeholder, value, onChange }) {
  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1">{placeholder}</label>
      <div className="flex items-center px-3 py-2 border rounded-lg bg-gray-50">
        {icon}
        <input
          type="text"
          name={name}
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          className="w-full bg-gray-50 outline-none"
          required
        />
      </div>
    </div>
  )
}

export default Register

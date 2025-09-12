import { useEffect, useState } from "react"
import { User, Mail, Phone, Shield, Lock } from "lucide-react"
import userService from "../../services/userService"
import toast from "react-hot-toast"

function Profile() {
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [showPasswordModal, setShowPasswordModal] = useState(false)
  const [passwordData, setPasswordData] = useState({ old_password: "", new_password: "" })
  const [passwordLoading, setPasswordLoading] = useState(false)

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await userService.getCurrentProfile()
        setProfile(res.data)
      } catch (err) {
        console.error("Fetch profile error:", err)
        toast.error("Không thể tải thông tin người dùng")
      }
    }
    fetchProfile()
  }, [])

  if (!profile) {
    return (
      <div className="min-h-screen w-full flex items-center justify-center bg-gray-100">
        <p className="text-gray-600">Đang tải thông tin...</p>
      </div>
    )
  }

  const handleChangeProfile = (e) => {
    const { name, value } = e.target
    setProfile(prev => ({ ...prev, [name]: value }))
  }

  const handleSaveProfile = async () => {
    setLoading(true)
    try {
      const res = await userService.updateProfile({
        name: profile.name,
        email: profile.email,
        phone_number: profile.phone_number
      })
      setProfile(res.data)
      toast.success("Cập nhật thông tin thành công!")
    } catch (err) {
      console.error(err)
      toast.error(err.response?.data?.message || err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleChangePassword = async () => {
    setPasswordLoading(true)
    try {
      const res = await userService.changePassword(passwordData.old_password, passwordData.new_password)
      toast.success(res.data.message || "Đổi mật khẩu thành công!")
      setPasswordData({ old_password: "", new_password: "" })
      setShowPasswordModal(false)
    } catch (err) {
      console.error(err)
      toast.error(err.response?.data?.message || err.message)
    } finally {
      setPasswordLoading(false)
    }
  }

  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-gray-100 px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-xl p-8">
        <div className="flex flex-col items-center mb-6">
          <div className="flex items-center justify-center w-16 h-16 rounded-full bg-gray-200 text-gray-600 mb-3">
            <User className="w-8 h-8" />
          </div>
          <h2 className="text-2xl font-bold text-gray-800">Thông tin cá nhân</h2>
          <p className="text-gray-500 text-sm">Cập nhật hồ sơ của bạn</p>
        </div>

        {/* Form profile */}
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Họ và tên</label>
            <div className="flex items-center px-3 py-2 border rounded-lg bg-gray-50">
              <User className="text-gray-400 mr-2" size={18} />
              <input
                type="text"
                name="name"
                value={profile.name}
                onChange={handleChangeProfile}
                className="w-full bg-gray-50 outline-none"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <div className="flex items-center px-3 py-2 border rounded-lg bg-gray-50">
              <Mail className="text-gray-400 mr-2" size={18} />
              <input
                type="email"
                name="email"
                value={profile.email}
                onChange={handleChangeProfile}
                className="w-full bg-gray-50 outline-none"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Số điện thoại</label>
            <div className="flex items-center px-3 py-2 border rounded-lg bg-gray-50">
              <Phone className="text-gray-400 mr-2" size={18} />
              <input
                type="text"
                name="phone_number"
                value={profile.phone_number}
                onChange={handleChangeProfile}
                className="w-full bg-gray-50 outline-none"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Vai trò</label>
            <div className="flex items-center px-3 py-2 border rounded-lg bg-gray-50">
              <Shield className="text-gray-400 mr-2" size={18} />
              <span className="text-gray-800 capitalize">{profile.role}</span>
            </div>
          </div>
        </div>

        <button
          type="button"
          onClick={handleSaveProfile}
          disabled={loading}
          className="w-full mt-6 py-2 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 disabled:opacity-50 transition-colors"
        >
          {loading ? "Đang lưu..." : "Lưu thay đổi"}
        </button>

        <button
          type="button"
          onClick={() => setShowPasswordModal(true)}
          className="w-full mt-3 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 flex items-center justify-center transition-colors"
        >
          <Lock className="mr-2" size={18} /> Đổi mật khẩu
        </button>

        {/* Modal đổi mật khẩu */}
        {showPasswordModal && (
          <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
            <div className="bg-white rounded-xl p-6 w-full max-w-sm shadow-lg">
              <h3 className="text-lg font-bold mb-4">Đổi mật khẩu</h3>
              <input
                type="password"
                placeholder="Mật khẩu cũ"
                value={passwordData.old_password}
                onChange={(e) => setPasswordData(prev => ({ ...prev, old_password: e.target.value }))}
                className="w-full mb-3 px-3 py-2 border rounded-lg outline-none"
              />
              <input
                type="password"
                placeholder="Mật khẩu mới"
                value={passwordData.new_password}
                onChange={(e) => setPasswordData(prev => ({ ...prev, new_password: e.target.value }))}
                className="w-full mb-3 px-3 py-2 border rounded-lg outline-none"
              />
              <div className="flex justify-end space-x-2">
                <button
                  onClick={() => setShowPasswordModal(false)}
                  className="px-3 py-2 border rounded-lg text-gray-700 hover:bg-gray-50"
                >
                  Hủy
                </button>
                <button
                  onClick={handleChangePassword}
                  disabled={passwordLoading}
                  className="px-3 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50"
                >
                  {passwordLoading ? "Đang lưu..." : "Lưu"}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Profile

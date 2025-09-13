import { useEffect, useState } from "react"
import { Search, ShoppingCart } from "lucide-react"
import { Button } from "./ui/button"
import { Input } from "./ui/input"
import { UserDropdown } from "./user-dropdown"
import { CartPanel } from "./cart-panel"

export function Header({ onSearch }) {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [user, setUser] = useState(null)

  const [filters, setFilters] = useState({
    title: "",
    location: "",
    start_time: "",
    end_time: "",
  })
 const [isCartOpen, setIsCartOpen] = useState(false)
 // Mock cart data - thay bằng data thực khi tích hợp backend
  const [cartData, setCartData] = useState({
    id: 1,
    user_id: 5,
    items: [
      {
        id: 1,
        event_id: 1,
        ticket_type: "VIP",
        quantity: 2,
        event: { title: "Concert A" },
      },
      {
        id: 2,
        event_id: 2,
        ticket_type: "Standard",
        quantity: 1,
        event: { title: "Concert B" },
      },
    ],
  })
  useEffect(() => {
    const token = localStorage.getItem("token")
    const expiredAt = localStorage.getItem("expired_at")
    const userData = localStorage.getItem("user")

    if (token && expiredAt) {
      const now = new Date().getTime()
      const exp = new Date(expiredAt).getTime()
      if (now < exp) {
        setIsLoggedIn(true)
        if (userData) {
          setUser(JSON.parse(userData))
        }
      } else {
        localStorage.removeItem("token")
        localStorage.removeItem("expired_at")
        localStorage.removeItem("user")
        setIsLoggedIn(false)
      }
    }
  }, [])

  const handleChange = (e) => {
    const { name, value } = e.target
    setFilters((prev) => ({ ...prev, [name]: value }))
  }

  const handleSearch = () => {
    if (onSearch) {
      onSearch(filters)
    }
  }

  return (
    <header className="bg-white shadow-sm border-b border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col gap-4 py-4">
          {/* Top row: Logo + User */}
          <div className="flex items-center justify-between">
            {/* Logo */}
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="flex items-center space-x-1">
                  <div className="w-8 h-8 bg-gradient-to-r from-pink-500 to-blue-500 rounded-full flex items-center justify-center">
                    <span className="text-white font-bold text-sm">C</span>
                  </div>
                  <span className="text-xl font-bold text-gray-900">Ticket</span>
                </div>
              </div>
            </div>

            {/* Right side */}
             <div className="flex items-center space-x-4">
              {isLoggedIn ? (
                <>
                  {/* Cart Button */}
                  <Button
                    variant="ghost"
                    size="sm"
                    className="relative"
                    onClick={() => setIsCartOpen(true)}
                  >
                    <ShoppingCart className="h-5 w-5 text-gray-700 hover:text-gray-900" />
                    {cartData.items.length > 0 && (
                      <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                        {cartData.items.length}
                      </span>
                    )}
                  </Button>

                  {/* UserDropdown */}
                  <UserDropdown isLoggedIn={true} user={user} />
                </>
              ) : (
                <>
                  <Button
                    variant="ghost"
                    size="sm"
                    className="text-gray-700 hover:text-gray-900"
                    onClick={() => (window.location.href = "/login")}
                  >
                    Login
                  </Button>
                  <Button
                    variant="ghost"
                    size="sm"
                    className="text-gray-700 hover:text-gray-900"
                    onClick={() => (window.location.href = "/register")}
                  >
                    Register
                  </Button>
                </>
              )}
            </div>
          </div>
            {/* Cart Panel */}
            <CartPanel
            isOpen={isCartOpen}
            onClose={() => setIsCartOpen(false)}
            cartData={cartData}
            />
          {/* Search row */}
        <div className="flex flex-wrap gap-3 items-center justify-center">
        <div className="relative flex-1 min-w-[200px]">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <Input
            type="text"
            name="title"
            placeholder="Search for events, artists..."
            value={filters.title}
            onChange={handleChange}
            className="pl-10 pr-4 py-2 w-full bg-gray-50 border-gray-200 focus:bg-white"
            />
        </div>

        <Input
            type="text"
            name="location"
            placeholder="Location..."
            value={filters.location}
            onChange={handleChange}
            className="w-40"
        />

        <div className="flex gap-3 w-full">
            <Input
                type="datetime-local"
                name="start_time"
                value={filters.start_time}
                onChange={handleChange}
                className="flex-1 min-w-[220px]"
            />
            <Input
                type="datetime-local"
                name="end_time"
                value={filters.end_time}
                onChange={handleChange}
                className="flex-1 min-w-[220px]"
            />
        </div>

        <Button onClick={handleSearch} className="bg-blue-600 text-white">
            Search
        </Button>

        <Button
            variant="outline"
            onClick={() => {
            const cleared = {
                title: "",
                location: "",
                start_time: "",
                end_time: "",
            }
            setFilters(cleared)
            if (onSearch) {
                onSearch(cleared)
            }
            }}
        >
            Reset
        </Button>
        </div>
        </div>
      </div>
    </header>
  )
}

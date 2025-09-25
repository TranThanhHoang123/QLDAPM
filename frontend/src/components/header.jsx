import { useEffect, useState } from "react"
import { ShoppingCart } from "lucide-react"
import { Button } from "./ui/button"
import { UserDropdown } from "./user-dropdown"
import { CartPanel } from "./cart-panel"
import { useCart } from "../contexts/CartContext"
export function Header() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [user, setUser] = useState(null)

 const [isCartOpen, setIsCartOpen] = useState(false)
 
  const { cartData } = useCart()
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
            />
        </div>
        </div>
    </header>
  )
}

import { createContext, useContext, useState, useEffect } from "react"
import cartService from "../services/cartService"

const CartContext = createContext()

export function CartProvider({ children }) {
  const [cartData, setCartData] = useState({ items: [] })

  useEffect(() => {
    async function fetchCart() {
      const res = await cartService.getList()
      if (res.data.items) {
        setCartData(res.data)
      } else {
        setCartData({ items: [] }) // fallback khi API chỉ trả message
      }
    }
    fetchCart()
  }, [])

  return (
    <CartContext.Provider value={{ cartData, setCartData }}>
      {children}
    </CartContext.Provider>
  )
}

export function useCart() {
  return useContext(CartContext)
}

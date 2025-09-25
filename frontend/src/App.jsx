import AppRoutes from "./routes"
import { Toaster } from "react-hot-toast"
import { CartProvider } from "./contexts/CartContext"

function App() {
  return (
    <CartProvider>
      <Toaster position="top-right" reverseOrder={false} />
      <AppRoutes />
    </CartProvider>
  )
}

export default App

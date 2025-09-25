import { X, Trash2 } from "lucide-react";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import cartService from "../services/cartService";
import { useCart } from "../contexts/CartContext"
import toast from "react-hot-toast"
export function CartPanel({ isOpen, onClose }) {
  const { cartData, setCartData } = useCart()
  const handleRemoveItem = async (itemId) => {
    try {
      await cartService.removeTicket(itemId);

      // cập nhật lại list item trong giỏ
      setCartData((prev) => ({
        ...prev,
        items: prev.items.filter((item) => item.id !== itemId),
      }));
      toast.success("Xóa thành công");
    } catch (err) {
      toast.error("Lỗi khi xóa item:", err);
    }
  };

  const calculateTotal = () => {
    return cartData.items.reduce((total, item) => {
      const mockPrice = item.ticket_type === "VIP" ? 150000 : 100000;
      return total + mockPrice * item.quantity;
    }, 0);
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat("vi-VN", {
      style: "currency",
      currency: "VND",
    }).format(price);
  };

  const isEmpty =
    !cartData ||
    cartData.message === "Cart is empty" ||
    !cartData.items ||
    cartData.items.length === 0;

  return (
    <>
      {/* Backdrop */}
      <div
        className={`fixed inset-0 bg-black/50 z-40 transition-opacity duration-300 ${
          isOpen ? "opacity-100" : "opacity-0 pointer-events-none"
        }`}
        onClick={onClose}
      />

      {/* Cart Panel */}
      <div
        className={`fixed right-0 top-0 h-full w-96 bg-white shadow-2xl z-50 transform transition-transform duration-300 ease-in-out ${
          isOpen ? "translate-x-0" : "translate-x-full"
        }`}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b">
          <h2 className="text-lg font-semibold text-gray-900">Your Cart</h2>
          <Button variant="ghost" size="sm" onClick={onClose}>
            <X className="h-5 w-5" />
          </Button>
        </div>

        {/* Cart Items */}
        <div className="flex-1 overflow-y-auto p-4">
          {isEmpty ? (
            <div className="text-center py-8">
              <p className="text-gray-500">Chưa có vé nào trong giỏ hàng</p>
            </div>
          ) : (
            <div className="space-y-4">
              {cartData.items.map((item) => (
                <div key={item.id} className="bg-gray-50 rounded-lg p-4">
                  <div className="flex justify-between items-center mb-2">
                    <h3 className="font-medium text-gray-900 text-sm">
                      {item.event.name}
                    </h3>
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => handleRemoveItem(item.id)}
                      className="text-red-500 hover:text-red-700 h-8 w-8 flex items-center justify-center"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>

                  <Badge variant="secondary" className="mb-2">
                    {item.ticket_type}
                  </Badge>

                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">
                      Số lượng: {item.quantity}
                    </span>
                    <span className="text-sm font-semibold text-gray-900">
                      {formatPrice(
                        (item.ticket_type === "VIP" ? 150000 : 100000) *
                          item.quantity
                      )}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        {!isEmpty && (
          <div className="border-t p-4 space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-lg font-semibold text-gray-900">Total:</span>
              <span className="text-lg font-bold text-cyan-600">
                {formatPrice(calculateTotal())}
              </span>
            </div>

            <Button className="w-full bg-gradient-to-r from-pink-500 to-blue-500 hover:from-pink-600 hover:to-blue-600 text-white">
              Proceed to Checkout
            </Button>
          </div>
        )}
      </div>
    </>
  );
}

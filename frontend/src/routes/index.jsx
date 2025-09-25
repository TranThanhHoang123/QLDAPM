import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "../pages/Home";
import Login from "../pages/Login";
import Dashboard from "../pages/Dashboard";
import PaymentResult from "../pages/Payment/PaymentResult"
import OrderDetail from "../pages/Order/OrderDetail"
import Order from "../pages/Order"
import Payment from "../pages/Payment/index"
import Profile from "../pages/Profile"
import Admin from "../pages/Admin"
import Register from "../pages/Register"
import EventDetail from "../pages/EventDetail"
import Checkout from "../pages/Checkout";
import Ticket from "../pages/Ticket";
import TicketDetail from "../pages/Ticket/TicketDetail"

function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/payment" element={<Payment />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/admin/*" element={<Admin />} /> 
        <Route path="/event/:id" element={<EventDetail />} />
        <Route path="/checkout" element={<Checkout />} />
        <Route path="/payment_result" element={<PaymentResult />} />
        <Route path="/orders/:id" element={<OrderDetail />} />
        <Route path="/orders" element={<Order />} />
        <Route path="/ticket" element={<Ticket />} />
        <Route path="/ticket/:id" element={<TicketDetail />} />
      </Routes>
    </BrowserRouter>
  );
}

export default AppRoutes;

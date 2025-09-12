import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "../pages/Home";
import Login from "../pages/Login";
import Dashboard from "../pages/Dashboard";
import Payment from "../pages/Payment";
import Profile from "../pages/Profile"
import Admin from "../pages/Admin"
import Register from "../pages/Register"

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
      </Routes>
    </BrowserRouter>
  );
}

export default AppRoutes;

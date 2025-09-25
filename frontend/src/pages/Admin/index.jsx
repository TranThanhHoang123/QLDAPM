import { Link, Routes, Route } from "react-router-dom"
import Event from "./Event"
import Dashboard from "./Dashboard"
import Employee from "./Employee"
import Category from "./Category"
import EventDetail from "./Event/EventDetail"

// Import icon từ lucide-react
import { Calendar, LayoutDashboard, Users, Folder } from "lucide-react"
import EventNew from "./Event/EventNew"
import AdminUser from "./Employee"
import UserForm from "./Employee/UserForm"

function Admin() {
  return (
    <div style={styles.container}>
      {/* Sidebar */}
      <aside style={styles.sidebar}>
        <h2 style={styles.logo}>Admin Panel</h2>
        <nav>
          <ul style={styles.menu}>
            <li style={styles.menuItem}>
              <Calendar size={18} style={styles.icon} />
              <Link to="/admin/event" style={styles.link}>Event</Link>
            </li>
            <li style={styles.menuItem}>
              <LayoutDashboard size={18} style={styles.icon} />
              <Link to="/admin/dashboard" style={styles.link}>Dashboard</Link>
            </li>
            <li style={styles.menuItem}>
              <Users size={18} style={styles.icon} />
              <Link to="/admin/employee" style={styles.link}>Employee</Link>
            </li>
            <li style={styles.menuItem}>
              <Folder size={18} style={styles.icon} />
              <Link to="/admin/category" style={styles.link}>Category</Link>
            </li>
          </ul>
        </nav>
      </aside>

      {/* Main Content */}
      <main style={styles.content}>
        <Routes>
          <Route path="event" element={<Event />} />
          <Route path="event/new" element={<EventNew />} />
          <Route path="event/detail/:id" element={<EventDetail />} /> {/* 👈 route chi tiết */}
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="employee" element={<Employee />} />
          <Route path="category" element={<Category />} />
          <Route index element={<h2>Chào mừng đến Admin Dashboard</h2>} />
          <Route path="user" element={<AdminUser />} />
          <Route path="user/new" element={<UserForm />} />
        </Routes>
      </main>
    </div>
  )
}

const styles = {
  container: {
    display: "flex",
    minHeight: "100vh",
  },
  sidebar: {
    width: "220px",
    background: "#1e293b",
    color: "#fff",
    padding: "1rem",
  },
  logo: {
    marginBottom: "2rem",
    fontSize: "1.2rem",
  },
  menu: {
    listStyle: "none",
    padding: 0,
    lineHeight: "2",
  },
  menuItem: {
    display: "flex",
    alignItems: "center",
    marginBottom: "1rem",
    gap: "8px",
  },
  icon: {
    color: "#e2e8f0",
  },
  link: {
    color: "#fff",
    textDecoration: "none",
  },
  content: {
    flex: 1,
    padding: "2rem",
    background: "#f1f5f9",
  },
}

export default Admin
import { Link, Routes, Route } from "react-router-dom";
import Event from "./Event";
import Dashboard from "./Dashboard";

function Admin() {
  return (
    <div style={styles.container}>
      {/* Sidebar */}
      <aside style={styles.sidebar}>
        <h2 style={styles.logo}>Admin Panel</h2>
        <nav>
          <ul style={styles.menu}>
            <li><Link to="/admin/event">👤 Event</Link></li>
            <li><Link to="/admin/dashboard">🔑 Dashboard</Link></li>
          </ul>
        </nav>
      </aside>

      {/* Main Content */}
      <main style={styles.content}>
        <Routes>
          <Route path="event" element={<Event />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route index element={<h2>Chào mừng đến Admin Dashboard</h2>} />
        </Routes>
      </main>
    </div>
  );
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
  content: {
    flex: 1,
    padding: "2rem",
    background: "#f1f5f9",
  },
};

export default Admin;

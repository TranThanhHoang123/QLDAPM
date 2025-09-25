import { Header } from "../components/header"
// Layout.jsx
export function Layout({ children }) {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main>{children}</main>
    </div>
  )
}

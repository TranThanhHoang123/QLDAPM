import { useEffect, useState } from "react"
import { HeroSection } from "@/components/hero-section"
import { SearchBar } from "@/components/search-bar"
import { EventsSection } from "@/components/events-section"
import categoryService from "../../services/categoryService"
import eventService from "../../services/eventService"
import { Layout } from "../layout"

export default function Home() {
  const [categories, setCategories] = useState([])
  const [events, setEvents] = useState([])
  const [filters, setFilters] = useState({})
  const [activeCategory, setActiveCategory] = useState(0)
  const [loading, setLoading] = useState(false) // thêm loading

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true) // bắt đầu loading

        // categories
        console.log("Fetching events with filters:", filters)
        const res = await categoryService.getList()
        setCategories([{ id: 0, name: "All Categories" }, ...res.data.items])

        // events
        const eventRes = await eventService.getList(filters)
        const mappedEvents = eventRes.data.items.map((e) => ({
          id: e.id,
          title: e.title,
          image: e.image,
          location: e.location,
          available_ticket_counts: e.available_ticket_counts || {},
          date: new Date(e.start_time).toLocaleString("vi-VN"),
          category: e.category?.name || "Uncategorized",
        }))
        setEvents(mappedEvents)
      } catch (err) {
        console.error("Error fetching data:", err)
      } finally {
        setLoading(false) // tắt loading
      }
    }
    fetchData()
  }, [filters])

  const handleCategoryChange = (categoryId) => {
    setActiveCategory(categoryId)
    setFilters((prev) => {
      if (categoryId === 0) {
        const { category_id, ...rest } = prev
        return rest
      } else {
        return { ...prev, category_id: categoryId }
      }
    })
  }

  return (
    <Layout>
      <HeroSection />
      <SearchBar
        initialFilters={filters}
        onSearch={(newFilters) => setFilters(newFilters)} // ✅ update filters => trigger useEffect => call API
        onReset={() => setFilters({})}                   // ✅ reset về rỗng
      />
      {loading ? (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex justify-center items-center z-50">
          <div className="animate-spin rounded-full h-12 w-12 border-4 border-white border-t-transparent"></div>
        </div>
      ) : (
        <EventsSection
          categories={categories}
          events={events}
          activeCategory={activeCategory}
          onCategoryChange={handleCategoryChange}
        />
      )}
    </Layout>
  )
}

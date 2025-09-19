import { Card, CardContent } from "./ui/card"
import { Badge } from "./ui/badge"

export function EventsSection({ categories = [], events = [], activeCategory = 0, onCategoryChange }) {
  return (
    <section className="py-16 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl font-extrabold tracking-tight text-gray-900 mb-10">
          Events
        </h2>

        {/* Category filters */}
        <div className="flex flex-wrap gap-3 mb-12">
          {categories.map((category) => (
            <Badge
              key={category.id}
              asChild
              className={`px-4 py-2 text-sm cursor-pointer transition-colors ${
                activeCategory === category.id
                  ? "bg-blue-600 text-white border-blue-600"
                  : "bg-gray-200 text-gray-700 hover:bg-blue-100 hover:text-blue-700"
              }`}
            >
              <button onClick={() => onCategoryChange?.(category.id)}>
                {category.name}
              </button>
            </Badge>
          ))}
        </div>

        {/* Events grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
          {events.map((event) => (
            <Card
              key={event.id}
              className="overflow-hidden hover:shadow-xl transition-shadow duration-300 cursor-pointer rounded-xl"
            >
              <div className="relative">
                <img
                  src={event.image || "/placeholder.svg"}
                  alt={event.title}
                  className="w-full h-52 object-cover"
                />
              </div>
              <CardContent className="p-5">
                <Badge variant="outline" className="mb-3 text-xs">
                  {event.category}
                </Badge>
                <h3 className="font-semibold text-base mb-2 line-clamp-2 text-gray-900">
                  {event.title}
                </h3>
                <p className="text-sm text-gray-500">
                  {event.location} — {event.date}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  )
}

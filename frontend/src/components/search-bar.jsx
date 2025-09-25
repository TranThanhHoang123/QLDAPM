import { useState } from "react"
import { Search } from "lucide-react"
import { Input } from "./ui/input"
import { Button } from "./ui/button"

export function SearchBar({ initialFilters = {}, onSearch, onReset }) {
  const [localFilters, setLocalFilters] = useState(initialFilters)

  const handleChange = (e) => {
    const { name, value } = e.target
    setLocalFilters((prev) => ({ ...prev, [name]: value }))
  }

  return (
    <div className="flex flex-wrap gap-3 items-center justify-center py-4">
      <div className="relative flex-1 min-w-[200px]">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
        <Input
          type="text"
          name="title"
          placeholder="Search for events, artists..."
          value={localFilters.title || ""}
          onChange={handleChange}
          className="pl-10 pr-4 py-2 w-full bg-gray-50 border-gray-200 focus:bg-white"
        />
      </div>

      {/* Location */}
      <Input
        type="text"
        name="location"
        placeholder="Location..."
        value={localFilters.location || ""}
        onChange={handleChange}
        className="w-40"
      />

      {/* Time range */}
      <div className="flex gap-3 w-full">
        <Input
          type="datetime-local"
          name="start_time"
          value={localFilters.start_time || ""}
          onChange={handleChange}
          className="flex-1 min-w-[220px]"
        />
        <Input
          type="datetime-local"
          name="end_time"
          value={localFilters.end_time || ""}
          onChange={handleChange}
          className="flex-1 min-w-[220px]"
        />
      </div>

      {/* Buttons */}
      <Button
        onClick={() => onSearch?.(localFilters)}
        className="bg-blue-600 text-white"
      >
        Search
      </Button>
      <Button
        variant="outline"
        onClick={() => {
          setLocalFilters({})
          onReset?.()
        }}
      >
        Reset
      </Button>
    </div>
  )
}

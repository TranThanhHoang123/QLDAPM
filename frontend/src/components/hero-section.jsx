import { ChevronLeft, ChevronRight } from "lucide-react"
import { Button } from "./ui/button"
import { useState } from "react"

export function HeroSection() {
  const [currentSlide, setCurrentSlide] = useState(0)
  const totalSlides = 5

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % totalSlides)
  }

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + totalSlides) % totalSlides)
  }

  return (
    <section className="relative h-[500px] bg-gradient-to-b from-cyan-400 to-cyan-500 overflow-hidden">
      {/* Sky and clouds background */}
      <div className="absolute inset-0">
        <div className="absolute top-8 left-20 w-16 h-10 bg-white rounded-full opacity-90 animate-float"></div>
        <div className="absolute top-12 right-32 w-20 h-12 bg-white rounded-full opacity-80 animate-float-delayed"></div>
        <div className="absolute top-20 left-1/3 w-12 h-8 bg-white rounded-full opacity-85 animate-float"></div>
        <div className="absolute top-6 right-20 w-14 h-9 bg-white rounded-full opacity-75 animate-float-delayed"></div>
      </div>

      {/* Rolling hills */}
      <div className="absolute bottom-0 left-0 right-0">
        <svg viewBox="0 0 1200 300" className="w-full h-auto">
          <path
            d="M0,300 C200,250 400,280 600,260 C800,240 1000,270 1200,250 L1200,300 Z"
            fill="#22c55e"
            className="drop-shadow-sm"
          />
          <path d="M0,300 C150,270 350,290 550,275 C750,260 950,285 1200,270 L1200,300 Z" fill="#16a34a" />
        </svg>
      </div>

      {/* Tree */}
      <div className="absolute bottom-16 left-20">
        <div className="w-2 h-16 bg-amber-800 rounded-t-full"></div>
        <div className="absolute -top-8 -left-6 w-14 h-14 bg-green-600 rounded-full"></div>
        <div className="absolute -top-6 -left-4 w-10 h-10 bg-green-500 rounded-full"></div>
        <div className="absolute -top-4 -left-8 w-12 h-12 bg-green-700 rounded-full"></div>
      </div>

      {/* Vintage van */}
      <div className="absolute bottom-20 left-1/2 transform -translate-x-1/2">
        <div className="relative">
          {/* Van body */}
          <div className="w-24 h-12 bg-yellow-400 rounded-t-lg border-2 border-yellow-500">
            {/* Windows */}
            <div className="flex space-x-1 mt-1 mx-2">
              <div className="w-4 h-3 bg-cyan-200 rounded-sm"></div>
              <div className="w-4 h-3 bg-cyan-200 rounded-sm"></div>
              <div className="w-4 h-3 bg-cyan-200 rounded-sm"></div>
            </div>
            {/* Luggage on top */}
            <div className="absolute -top-3 left-2 w-6 h-2 bg-amber-700 rounded"></div>
            <div className="absolute -top-3 right-2 w-4 h-2 bg-red-600 rounded"></div>
          </div>
          {/* Wheels */}
          <div className="absolute -bottom-2 left-2 w-4 h-4 bg-gray-800 rounded-full"></div>
          <div className="absolute -bottom-2 right-2 w-4 h-4 bg-gray-800 rounded-full"></div>
        </div>
      </div>

      {/* Tent */}
      <div className="absolute bottom-16 left-32">
        <div className="w-8 h-6 bg-blue-500 rounded-t-full border-b-2 border-blue-600"></div>
        <div className="absolute top-4 left-1 w-6 h-1 bg-blue-600"></div>
      </div>

      {/* Pinwheels */}
      <div className="absolute bottom-20 right-32">
        <div className="flex space-x-4">
          <div className="w-3 h-8 bg-green-600 rounded-full relative">
            <div className="absolute -top-2 -left-1 w-5 h-5 bg-red-500 rounded-full animate-spin-slow"></div>
          </div>
          <div className="w-3 h-6 bg-green-600 rounded-full relative">
            <div className="absolute -top-2 -left-1 w-5 h-5 bg-yellow-500 rounded-full animate-spin-slow"></div>
          </div>
          <div className="w-3 h-10 bg-green-600 rounded-full relative">
            <div className="absolute -top-2 -left-1 w-5 h-5 bg-blue-500 rounded-full animate-spin-slow"></div>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="relative z-10 flex flex-col items-center justify-center h-full text-center">
        <div className="mb-4">
          <div className="text-4xl font-bold text-white mb-2">THE NEXT</div>
          <div className="text-sm text-white/90">Live Concert</div>
        </div>

        <div className="text-5xl font-bold text-white mb-4">25.10.2025 - HÀ NỘI</div>

        <div className="text-sm text-white/80 mb-8">
          THE NEXT live concert produced by GB Vietnam
          <br />
          Email: thenext@gbvietnam.com.vn
        </div>
      </div>

      {/* Navigation arrows */}
      <Button
        variant="ghost"
        size="icon"
        className="absolute left-4 top-1/2 transform -translate-y-1/2 bg-white/20 hover:bg-white/30 text-white"
        onClick={prevSlide}
      >
        <ChevronLeft className="h-6 w-6" />
      </Button>

      <Button
        variant="ghost"
        size="icon"
        className="absolute right-4 top-1/2 transform -translate-y-1/2 bg-white/20 hover:bg-white/30 text-white"
        onClick={nextSlide}
      >
        <ChevronRight className="h-6 w-6" />
      </Button>

      {/* Slide indicators */}
      <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex space-x-2">
        {Array.from({ length: totalSlides }).map((_, index) => (
          <button
            key={index}
            className={`w-2 h-2 rounded-full transition-colors ${index === currentSlide ? "bg-white" : "bg-white/50"}`}
            onClick={() => setCurrentSlide(index)}
          />
        ))}
      </div>
    </section>
  )
}

export function Avatar({ children, className }) {
  return (
    <div className={`relative flex items-center justify-center overflow-hidden rounded-full bg-gray-200 ${className}`}>
      {children}
    </div>
  )
}

export function AvatarImage({ src, alt }) {
  return (
    <img src={src} alt={alt} className="h-full w-full object-cover" />
  )
}

export function AvatarFallback({ children, className }) {
  return (
    <div className={`flex h-full w-full items-center justify-center text-sm font-medium ${className}`}>
      {children}
    </div>
  )
}

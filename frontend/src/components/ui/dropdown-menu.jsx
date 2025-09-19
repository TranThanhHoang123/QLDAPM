import { useState, useRef, useEffect } from "react"

function cn(...classes) {
  return classes.filter(Boolean).join(" ")
}

export function DropdownMenu({ children }) {
  const [open, setOpen] = useState(false)
  const menuRef = useRef(null)

  useEffect(() => {
    function handleClickOutside(e) {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        setOpen(false)
      }
    }
    document.addEventListener("mousedown", handleClickOutside)
    return () => document.removeEventListener("mousedown", handleClickOutside)
  }, [])

  // clone props open/setOpen cho tất cả children
  return (
    <div ref={menuRef} className="relative inline-block">
      {children &&
        (Array.isArray(children) ? children : [children]).map((child, i) =>
          child
            ? { ...child, props: { ...child.props, open, setOpen, key: i } }
            : null
        )}
    </div>
  )
}

export function DropdownMenuTrigger({ children, asChild, open, setOpen }) {
  return (
    <div onClick={() => setOpen(!open)} className="cursor-pointer inline-block">
      {children}
    </div>
  )
}

export function DropdownMenuContent({ children, open, align = "start", className = "" }) {
  if (!open) return null
  return (
    <div
      className={cn(
        "absolute z-50 mt-2 rounded-md border bg-white shadow-lg",
        align === "end" ? "right-0" : "left-0",
        className
      )}
    >
      <div className="p-1">{children}</div>
    </div>
  )
}
DropdownMenuContent.displayName = "DropdownMenuContent"

export function DropdownMenuItem({ children, onClick, className = "" }) {
  return (
    <div
      onClick={onClick}
      className={cn(
        "flex items-center px-3 py-2 text-sm rounded-md cursor-pointer hover:bg-gray-100",
        className
      )}
    >
      {children}
    </div>
  )
}

export function DropdownMenuSeparator() {
  return <div className="my-1 h-px bg-gray-200" />
}

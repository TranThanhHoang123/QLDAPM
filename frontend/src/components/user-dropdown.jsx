import { LogOut, Eye } from "lucide-react"
import { Button } from "./ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "./ui/dropdown-menu"

export function UserDropdown({ isLoggedIn, user }) {

  if (!isLoggedIn) {
    return null
  }

  const handleLogout = () => {
    localStorage.clear()
    window.location.href = "/" // chuyển về trang chủ
  }

  const handleViewDetails = () => {
    window.location.href = "/profile"
  }

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button
          variant="ghost"
          className="relative h-10 w-10 p-0 rounded-full overflow-hidden hover:bg-gray-100"
        >
          <span className="flex h-full w-full items-center justify-center rounded-full bg-gradient-to-r from-pink-500 to-blue-500 text-white font-semibold">
            {user?.name?.charAt(0).toUpperCase() || "U"}
          </span>
        </Button>
      </DropdownMenuTrigger>

      <DropdownMenuContent align="end" className="w-56">
        <div className="flex items-center gap-2 p-2">
          <div className="flex flex-col space-y-1 leading-none">
            {user?.name && <p className="font-medium text-sm">{user.name}</p>}
            {user?.email && (
              <p className="w-[200px] truncate text-xs text-gray-500">{user.email}</p>
            )}
          </div>
        </div>
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={handleViewDetails}>
          <Eye className="mr-2 h-4 w-4" />
          <span>Profile</span>
        </DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuItem
          onClick={handleLogout}
          className="text-red-600 hover:bg-red-50"
        >
          <LogOut className="mr-2 h-4 w-4" />
          <span>Logout</span>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}

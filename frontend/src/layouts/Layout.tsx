import { Link, Outlet } from 'react-router-dom'

export default function Layout() {
  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center gap-6">
          <Link to="/" className="text-xl font-bold text-indigo-600">GitPulse AI</Link>
          <Link to="/repositories" className="text-gray-600 hover:text-gray-900">مخازن</Link>
          <Link to="/settings" className="text-gray-600 hover:text-gray-900">تنظیمات</Link>

        </div>
      </nav>
      <main className="max-w-7xl mx-auto px-4 py-6">
        <Outlet />
      </main>
    </div>
  )
}
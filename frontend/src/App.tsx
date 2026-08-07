import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import Layout from './layouts/Layout'
import Dashboard from './pages/Dashboard'
import Repositories from './pages/Repositories'
import RepositoryDetail from './pages/RepositoryDetail'
import Settings from './pages/Settings'


const queryClient = new QueryClient()

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Dashboard />} />
            <Route path="repositories" element={<Repositories />} />
            <Route path="repositories/:id" element={<RepositoryDetail />} />
            <Route path="settings" element={<Settings />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}

export default App
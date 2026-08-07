import { useQuery } from '@tanstack/react-query'
import axios from 'axios'

export default function Dashboard() {
  const { data: repos } = useQuery({
    queryKey: ['repos'],
    queryFn: () => axios.get('/api/v1/repositories/').then(res => res.data),
  })

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">داشبورد</h1>
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-white p-4 rounded-lg shadow">
          <h2 className="text-lg font-semibold">تعداد کل مخازن</h2>
          <p className="text-3xl">{repos?.length || 0}</p>
        </div>
      </div>
    </div>
  )
}
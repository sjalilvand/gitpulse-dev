import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import axios from 'axios'

export default function Repositories() {
  const { data, isLoading } = useQuery({
    queryKey: ['repos'],
    queryFn: () => axios.get('/api/v1/repositories/').then(res => res.data),
  })

  if (isLoading) return <div className="p-4">در حال بارگذاری...</div>

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">مخازن</h1>
      <div className="grid gap-4">
        {data?.map((repo: any) => (
          <div key={repo.id} className="bg-white p-4 rounded-lg shadow">
            <Link
              to={`/repositories/${repo.id}`}
              className="text-xl font-semibold text-indigo-600 hover:underline"
            >
              {repo.full_name}
            </Link>
            <p className="text-gray-600 mt-1">{repo.description}</p>
            <div className="flex gap-4 mt-2 text-sm text-gray-500">
              <span>⭐ {repo.stars}</span>
              <span>🍴 {repo.forks}</span>
              <span>⚠️ {repo.open_issues_count} مسئله</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
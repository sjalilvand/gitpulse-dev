import { useQuery } from '@tanstack/react-query'
import axios from 'axios'
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts'

const COLORS = { open: '#22c55e', closed: '#ef4444' }
const STATE_NAMES: any = { open: 'باز', closed: 'بسته' }

export default function IssueList({ repoId }: { repoId: number }) {
  const { data: issues, isLoading } = useQuery({
    queryKey: ['issues', repoId],
    queryFn: () => axios.get(`/api/v1/issues/?repo_id=${repoId}`).then(res => res.data),
  })

  if (isLoading) return <div>در حال بارگذاری مسائل...</div>

  const stateCounts = issues.reduce((acc: any, iss: any) => {
    acc[iss.state] = (acc[iss.state] || 0) + 1
    return acc
  }, {})
  const chartData = Object.entries(stateCounts).map(([name, value]) => ({ name: STATE_NAMES[name] || name, value }))

  return (
    <div>
      <h3 className="text-lg font-semibold mb-2">مسائل</h3>
      {issues.length > 0 && (
        <div className="h-48 mb-4">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie data={chartData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label>
                {chartData.map((entry: any, index: number) => (
                  <Cell key={index} fill={COLORS[entry.name === 'باز' ? 'open' : 'closed'] || '#888'} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      )}
      <div className="space-y-2">
        {issues?.map((issue: any) => (
          <div key={issue.id} className="bg-white p-3 rounded shadow-sm">
            <span className={`px-2 py-1 text-xs rounded-full ${issue.state === 'open' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
              {issue.state === 'open' ? 'باز' : 'بسته'}
            </span>
            <span className="ml-2 font-medium">#{issue.number} {issue.title}</span>
            <div className="text-sm text-gray-600 mt-1">توسط {issue.author_username}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
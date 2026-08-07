import { useQuery } from '@tanstack/react-query'
import axios from 'axios'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

export default function CommitAnalytics({ repoId }: { repoId: number }) {
  const { data: commits, isLoading } = useQuery({
    queryKey: ['commits', repoId],
    queryFn: () => axios.get(`/api/v1/commits/?repo_id=${repoId}`).then(res => res.data),
  })

  if (isLoading) return <div>در حال بارگذاری کامیت‌ها...</div>

  const commitsPerDay = commits.reduce((acc: any, commit: any) => {
    const day = commit.committed_at.split('T')[0]
    acc[day] = (acc[day] || 0) + 1
    return acc
  }, {})
  const chartData = Object.entries(commitsPerDay).map(([day, count]) => ({ day, count }))

  return (
    <div>
      <h3 className="text-lg font-semibold mb-2">فعالیت کامیت‌ها</h3>
      <div className="h-64 mb-6">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="day" />
            <YAxis allowDecimals={false} />
            <Tooltip />
            <Bar dataKey="count" fill="#6366f1" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <h4 className="font-medium mb-2">کامیت‌های اخیر</h4>
      <div className="space-y-2 max-h-96 overflow-y-auto">
        {commits.slice(0, 20).map((commit: any) => (
          <div key={commit.commit_hash} className="bg-gray-50 p-2 rounded text-sm">
            <span className="font-mono text-xs text-gray-500">{commit.commit_hash.substring(0, 7)}</span>
            <span className="ml-2 font-medium">{commit.author_username}</span>
            <p className="text-gray-700 mt-1">{commit.message.split('\n')[0]}</p>
            <div className="text-xs text-gray-400">
              +{commit.additions} / -{commit.deletions} • {commit.files_changed} فایل
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
import { useParams } from 'react-router-dom'
import { useQuery, useMutation } from '@tanstack/react-query'
import axios from 'axios'
import CommitAnalytics from '../components/CommitAnalytics'
import PullRequestList from '../components/PullRequestList'
import IssueList from '../components/IssueList'
import { useState } from 'react'

export default function RepositoryDetail() {
  const { id } = useParams()
  const [tab, setTab] = useState<'commits' | 'prs' | 'issues' | 'ai'>('commits')

  const { data: repo } = useQuery({
    queryKey: ['repo', id],
    queryFn: () => axios.get(`/api/v1/repositories/${id}`).then(res => res.data),
  })

  const weeklySummaryMutation = useMutation({
    mutationFn: () => axios.post(`/api/v1/ai/repositories/${id}/weekly-summary`).then(res => res.data),
  })

  if (!repo) return <div>در حال بارگذاری...</div>

  return (
    <div>
      <h1 className="text-2xl font-bold mb-2">{repo.full_name}</h1>
      <p className="text-gray-600 mb-4">{repo.description}</p>
      <div className="flex gap-2 mb-4">
        <span className="bg-yellow-100 px-2 py-1 rounded">⭐ {repo.stars}</span>
        <span className="bg-gray-100 px-2 py-1 rounded">🍴 {repo.forks}</span>
        <span className="bg-red-100 px-2 py-1 rounded">⚠️ {repo.open_issues_count} مسئله</span>
      </div>

      {/* تب‌ها */}
      <div className="flex gap-4 border-b mb-4">
        {(['commits', 'prs', 'issues', 'ai'] as const).map(t => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`px-3 py-2 font-medium ${tab === t ? 'border-b-2 border-indigo-600 text-indigo-600' : 'text-gray-500'}`}
          >
            {t === 'commits' ? 'کامیت‌ها' : t === 'prs' ? 'درخواست‌های ادغام' : t === 'issues' ? 'مسائل' : 'گزارش‌های هوش مصنوعی'}
          </button>
        ))}
      </div>

      {/* محتوای تب */}
      {tab === 'commits' && <CommitAnalytics repoId={Number(id)} />}
      {tab === 'prs' && <PullRequestList repoId={Number(id)} />}
      {tab === 'issues' && <IssueList repoId={Number(id)} />}
      {tab === 'ai' && (
        <div className="space-y-4">
          <div className="bg-white p-4 rounded shadow">
            <h3 className="text-lg font-semibold mb-2">خلاصه هفتگی</h3>
            <button
              onClick={() => weeklySummaryMutation.mutate()}
              disabled={weeklySummaryMutation.isPending}
              className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700 disabled:opacity-50"
            >
              {weeklySummaryMutation.isPending ? 'در حال تولید...' : 'تولید خلاصه هفتگی'}
            </button>
            {weeklySummaryMutation.data && (
              <div className="mt-4 p-3 bg-gray-50 rounded whitespace-pre-wrap">
                {weeklySummaryMutation.data.summary}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
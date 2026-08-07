import { useQuery, useMutation } from '@tanstack/react-query'
import axios from 'axios'
import { useState } from 'react'

export default function PullRequestList({ repoId }: { repoId: number }) {
  const { data: prs, isLoading } = useQuery({
    queryKey: ['prs', repoId],
    queryFn: () => axios.get(`/api/v1/pull-requests/?repo_id=${repoId}`).then(res => res.data),
  })

  // ذخیره‌ی نتایج تحلیل به ازای هر PR
  const [analysisResults, setAnalysisResults] = useState<Record<number, any>>({})

  const analyzeMutation = useMutation({
    mutationFn: (prId: number) =>
      axios.post(`/api/v1/ai/pull-requests/${prId}/risk-analysis`).then(res => res.data),
    onSuccess: (data, variables) => {
      setAnalysisResults(prev => ({ ...prev, [variables]: data }))
    },
  })

  if (isLoading) return <div>در حال بارگذاری درخواست‌های ادغام...</div>

  return (
    <div>
      <h3 className="text-lg font-semibold mb-2">درخواست‌های ادغام</h3>
      <div className="space-y-2">
        {prs?.map((pr: any) => {
          const analysis = analysisResults[pr.id]
          return (
            <div key={pr.id} className="bg-white p-3 rounded shadow-sm">
              <div className="flex items-center gap-2">
                <span className={`px-2 py-1 text-xs rounded-full ${
                  pr.state === 'open' ? 'bg-green-100 text-green-800' :
                  pr.state === 'closed' ? 'bg-red-100 text-red-800' : 'bg-purple-100 text-purple-800'
                }`}>
                  {pr.state === 'open' ? 'باز' : pr.state === 'closed' ? 'بسته' : 'ادغام‌شده'}
                </span>
                <span className="font-medium">#{pr.number} {pr.title}</span>
              </div>
              <div className="text-sm text-gray-600 mt-1">
                توسط {pr.author_username} • +{pr.additions} -{pr.deletions} • {pr.changed_files} فایل
              </div>

              {/* دکمه تحلیل ریسک */}
              <div className="mt-2 flex items-center gap-2">
                <button
                  onClick={() => analyzeMutation.mutate(pr.id)}
                  disabled={analyzeMutation.isPending}
                  className="text-xs bg-yellow-500 text-white px-2 py-1 rounded hover:bg-yellow-600 disabled:opacity-50"
                >
                  {analyzeMutation.isPending ? 'در حال تحلیل...' : 'تحلیل ریسک'}
                </button>
                {pr.risk_score > 0 && !analysis && (
                  <span className="text-xs bg-yellow-50 text-yellow-700 px-2 py-1 rounded">
                    امتیاز قبلی: {pr.risk_score}/100
                  </span>
                )}
              </div>

              {/* نمایش نتیجه تحلیل */}
              {analysis && (
                <div className="mt-3 p-3 bg-gray-50 rounded text-sm space-y-2">
                  <div className="flex items-center gap-2">
                    <span className={`font-bold ${
                      analysis.risk_level === 'high' ? 'text-red-600' :
                      analysis.risk_level === 'medium' ? 'text-yellow-600' : 'text-green-600'
                    }`}>
                      ریسک: {analysis.risk_level === 'high' ? 'بالا' : analysis.risk_level === 'medium' ? 'متوسط' : 'پایین'}
                    </span>
                    <span className="text-gray-500">(امتیاز: {analysis.risk_score}/100)</span>
                  </div>
                  {analysis.summary && <p className="text-gray-700">{analysis.summary}</p>}
                  {analysis.risks && analysis.risks.length > 0 && (
                    <div>
                      <span className="font-medium">هشدارها:</span>
                      <ul className="list-disc list-inside text-gray-600">
                        {analysis.risks.map((r: string, i: number) => <li key={i}>{r}</li>)}
                      </ul>
                    </div>
                  )}
                  {analysis.suggestions && analysis.suggestions.length > 0 && (
                    <div>
                      <span className="font-medium">پیشنهادها:</span>
                      <ul className="list-disc list-inside text-gray-600">
                        {analysis.suggestions.map((s: string, i: number) => <li key={i}>{s}</li>)}
                      </ul>
                    </div>
                  )}
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
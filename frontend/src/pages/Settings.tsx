import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import axios from 'axios'

export default function Settings() {
  const queryClient = useQueryClient()

  // دریافت وضعیت scheduler
  const { data: status, isLoading } = useQuery({
    queryKey: ['scheduler-status'],
    queryFn: () => axios.get('/api/v1/scheduler/status').then(res => res.data),
    refetchInterval: 10000, // هر ۱۰ ثانیه بروزرسانی
  })

  // mutation برای اجرای همگام‌سازی دستی
  const manualSyncMutation = useMutation({
    mutationFn: () => axios.post('/api/v1/scheduler/trigger-sync'),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['scheduler-status'] })
    },
  })

  // mutation برای روشن/خاموش کردن خودکار
  const toggleAutoSyncMutation = useMutation({
    mutationFn: () => axios.post('/api/v1/scheduler/toggle-auto-sync'),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['scheduler-status'] })
    },
  })

  if (isLoading) return <div>در حال بارگذاری...</div>

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">تنظیمات همگام‌ساز</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div className="bg-white p-4 rounded-lg shadow">
          <h2 className="font-semibold text-lg mb-2">وضعیت</h2>
          <p>همگام‌سازی خودکار:
            <span className={`ml-2 px-2 py-1 rounded-full text-xs ${status?.auto_sync_enabled ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
              {status?.auto_sync_enabled ? 'فعال' : 'غیرفعال'}
            </span>
          </p>
          <p className="mt-2">Scheduler:
            <span className={`ml-2 px-2 py-1 rounded-full text-xs ${status?.scheduler_running ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
              {status?.scheduler_running ? 'در حال اجرا' : 'متوقف'}
            </span>
          </p>
          <p className="mt-2">آخرین همگام‌سازی:
            <span className="ml-2 font-medium">
              {status?.last_sync_time ? new Date(status.last_sync_time).toLocaleString('fa-IR') : 'هنوز اجرا نشده'}
            </span>
          </p>
        </div>

        <div className="bg-white p-4 rounded-lg shadow flex flex-col justify-center gap-3">
          <button
            onClick={() => manualSyncMutation.mutate()}
            disabled={manualSyncMutation.isPending}
            className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700 disabled:opacity-50"
          >
            {manualSyncMutation.isPending ? 'در حال همگام‌سازی...' : 'همگام‌سازی دستی'}
          </button>
          <button
            onClick={() => toggleAutoSyncMutation.mutate()}
            disabled={toggleAutoSyncMutation.isPending}
            className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700 disabled:opacity-50"
          >
            {status?.auto_sync_enabled ? 'غیرفعال کردن خودکار' : 'فعال کردن خودکار'}
          </button>
        </div>
      </div>
    </div>
  )
}
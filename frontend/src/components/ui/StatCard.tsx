import { ReactNode } from 'react'

interface StatCardProps {
  title: string
  value: number | string
  icon: ReactNode
  color: 'primary' | 'success' | 'warning' | 'danger' | 'violet'
}

const colors = {
  primary: { bg: 'bg-primary-100', text: 'text-primary-700' },
  success: { bg: 'bg-success-100', text: 'text-success-700' },
  warning: { bg: 'bg-warning-100', text: 'text-warning-700' },
  danger: { bg: 'bg-danger-100', text: 'text-danger-700' },
  violet: { bg: 'bg-accent-100', text: 'text-accent-700' },
}

export default function StatCard({ title, value, icon, color }: StatCardProps) {
  const c = colors[color]
  return (
    <div className="card p-5 flex items-center gap-4">
      <div className={`${c.bg} ${c.text} stat-icon`}>
        {icon}
      </div>
      <div>
        <p className="text-sm text-gray-500 font-medium">{title}</p>
        <p className="text-2xl font-bold text-gray-900">{value}</p>
      </div>
    </div>
  )
}
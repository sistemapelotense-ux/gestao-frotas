import { ReactNode } from 'react'

interface BadgeProps {
  color?: 'green' | 'yellow' | 'red' | 'blue' | 'violet' | 'gray'
  children: ReactNode
}

const colors = {
  green: 'badge-green',
  yellow: 'badge-yellow',
  red: 'badge-red',
  blue: 'badge-blue',
  violet: 'badge-violet',
  gray: 'badge-gray',
}

export default function Badge({ color = 'gray', children }: BadgeProps) {
  return <span className={colors[color]}>{children}</span>
}
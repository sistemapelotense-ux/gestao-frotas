import { useState, useEffect, useCallback } from 'react'
import type { DashboardResumo } from '../types'
import { getDashboardResumo } from '../services/dashboard'
import { handleApiError } from '../services/api'

export function useDashboard() {
  const [resumo, setResumo] = useState<DashboardResumo | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const result = await getDashboardResumo()
      setResumo(result)
    } catch (e) {
      setError(handleApiError(e))
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { load() }, [load])

  return { resumo, loading, error, load }
}
import { useState, useEffect, useCallback } from 'react'
import type { LancamentoDiario } from '../types'
import { listLancamentos, createLancamento, updateLancamento, deleteLancamento } from '../services/lancamentos'
import { handleApiError } from '../services/api'

export function useLancamentos() {
  const [lancamentos, setLancamentos] = useState<LancamentoDiario[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const result = await listLancamentos()
      setLancamentos(result)
    } catch (e) {
      setError(handleApiError(e))
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { load() }, [load])

  const create = async (payload: Partial<LancamentoDiario>) => {
    await createLancamento(payload)
    await load()
  }

  const update = async (id: string, payload: Partial<LancamentoDiario>) => {
    await updateLancamento(id, payload)
    await load()
  }

  const remove = async (id: string) => {
    await deleteLancamento(id)
    await load()
  }

  return { lancamentos, loading, error, load, create, update, remove }
}
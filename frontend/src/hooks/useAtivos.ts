import { useState, useEffect, useCallback } from 'react'
import type { Ativo } from '../types'
import { listAtivos, createAtivo, updateAtivo, deleteAtivo } from '../services/ativos'
import { handleApiError } from '../services/api'

export function useAtivos(search?: string) {
  const [ativos, setAtivos] = useState<Ativo[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const result = await listAtivos(0, 500, search)
      setAtivos(result)
    } catch (e) {
      setError(handleApiError(e))
    } finally {
      setLoading(false)
    }
  }, [search])

  useEffect(() => { load() }, [load])

  const create = async (payload: Partial<Ativo>) => {
    await createAtivo(payload)
    await load()
  }

  const update = async (id: string, payload: Partial<Ativo>) => {
    await updateAtivo(id, payload)
    await load()
  }

  const remove = async (id: string) => {
    await deleteAtivo(id)
    await load()
  }

  return { ativos, loading, error, load, create, update, remove }
}
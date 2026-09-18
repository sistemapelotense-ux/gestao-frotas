import { useState, useEffect, useCallback } from 'react'
import type { Obra } from '../types'
import { listObras, createObra, updateObra, deleteObra } from '../services/obras'
import { handleApiError } from '../services/api'

export function useObras(search?: string) {
  const [obras, setObras] = useState<Obra[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const result = await listObras(0, 500, search)
      setObras(result)
    } catch (e) {
      setError(handleApiError(e))
    } finally {
      setLoading(false)
    }
  }, [search])

  useEffect(() => { load() }, [load])

  const create = async (payload: Partial<Obra>) => {
    await createObra(payload)
    await load()
  }

  const update = async (id: string, payload: Partial<Obra>) => {
    await updateObra(id, payload)
    await load()
  }

  const remove = async (id: string) => {
    await deleteObra(id)
    await load()
  }

  return { obras, loading, error, load, create, update, remove }
}
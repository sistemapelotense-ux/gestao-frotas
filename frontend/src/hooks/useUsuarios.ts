import { useState, useEffect, useCallback } from 'react'
import type { Usuario } from '../types'
import { listUsuarios, createUsuario, updateUsuario, deleteUsuario } from '../services/usuarios'
import { handleApiError } from '../services/api'

export function useUsuarios() {
  const [usuarios, setUsuarios] = useState<Usuario[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const result = await listUsuarios()
      setUsuarios(result)
    } catch (e) {
      setError(handleApiError(e))
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { load() }, [load])

  const create = async (payload: Partial<Usuario>) => {
    await createUsuario(payload)
    await load()
  }

  const update = async (id: string, payload: Partial<Usuario>) => {
    await updateUsuario(id, payload)
    await load()
  }

  const remove = async (id: string) => {
    await deleteUsuario(id)
    await load()
  }

  return { usuarios, loading, error, load, create, update, remove }
}
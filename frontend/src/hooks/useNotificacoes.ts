import { useState, useEffect, useCallback } from 'react'
import type { Notificacao } from '../types'
import { listNotificacoes, countNaoLidas, marcarComoLida, marcarTodasComoLidas } from '../services/notificacoes'
import { handleApiError } from '../services/api'

export function useNotificacoes() {
  const [notificacoes, setNotificacoes] = useState<Notificacao[]>([])
  const [naoLidas, setNaoLidas] = useState(0)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const [lista, count] = await Promise.all([listNotificacoes(), countNaoLidas()])
      setNotificacoes(lista)
      setNaoLidas(count)
    } catch (e) {
      setError(handleApiError(e))
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { load() }, [load])

  const markRead = async (id: string) => {
    await marcarComoLida(id)
    await load()
  }

  const markAll = async () => {
    await marcarTodasComoLidas()
    await load()
  }

  return { notificacoes, naoLidas, loading, error, load, markRead, markAll }
}
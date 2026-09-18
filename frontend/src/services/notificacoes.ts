import { api } from './api'
import type { Notificacao } from '../types'

export async function listNotificacoes(lida?: boolean): Promise<Notificacao[]> {
  const { data } = await api.get<Notificacao[]>('/notificacoes', { params: { lida } })
  return data
}

export async function countNaoLidas(): Promise<number> {
  const { data } = await api.get<{ nao_lidas: number }>('/notificacoes/count')
  return data.nao_lidas
}

export async function marcarComoLida(id: string): Promise<void> {
  await api.put(`/notificacoes/${id}/ler`)
}

export async function marcarTodasComoLidas(): Promise<void> {
  await api.put('/notificacoes/ler-todas')
}
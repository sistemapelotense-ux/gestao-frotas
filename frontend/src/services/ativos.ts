import { api } from './api'
import type { Ativo } from '../types'

export async function listAtivos(skip = 0, limit = 100, search?: string): Promise<Ativo[]> {
  const { data } = await api.get<Ativo[]>('/ativos', { params: { skip, limit, search } })
  return data
}

export async function getAtivo(id: string): Promise<Ativo> {
  const { data } = await api.get<Ativo>(`/ativos/${id}`)
  return data
}

export async function createAtivo(payload: Partial<Ativo>): Promise<Ativo> {
  const { data } = await api.post<Ativo>('/ativos', payload)
  return data
}

export async function updateAtivo(id: string, payload: Partial<Ativo>): Promise<Ativo> {
  const { data } = await api.put<Ativo>(`/ativos/${id}`, payload)
  return data
}

export async function deleteAtivo(id: string): Promise<void> {
  await api.delete(`/ativos/${id}`)
}
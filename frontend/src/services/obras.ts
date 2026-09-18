import { api } from './api'
import type { Obra } from '../types'

export async function listObras(skip = 0, limit = 100, search?: string): Promise<Obra[]> {
  const { data } = await api.get<Obra[]>('/obras', { params: { skip, limit, search } })
  return data
}

export async function getObra(id: string): Promise<Obra> {
  const { data } = await api.get<Obra>(`/obras/${id}`)
  return data
}

export async function createObra(payload: Partial<Obra>): Promise<Obra> {
  const { data } = await api.post<Obra>('/obras', payload)
  return data
}

export async function updateObra(id: string, payload: Partial<Obra>): Promise<Obra> {
  const { data } = await api.put<Obra>(`/obras/${id}`, payload)
  return data
}

export async function deleteObra(id: string): Promise<void> {
  await api.delete(`/obras/${id}`)
}
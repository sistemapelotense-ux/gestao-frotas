import { api } from './api'
import type { LancamentoDiario } from '../types'

export async function listLancamentos(skip = 0, limit = 100): Promise<LancamentoDiario[]> {
  const { data } = await api.get<LancamentoDiario[]>('/lancamentos', { params: { skip, limit } })
  return data
}

export async function getLancamento(id: string): Promise<LancamentoDiario> {
  const { data } = await api.get<LancamentoDiario>(`/lancamentos/${id}`)
  return data
}

export async function createLancamento(payload: Partial<LancamentoDiario>): Promise<LancamentoDiario> {
  const { data } = await api.post<LancamentoDiario>('/lancamentos', payload)
  return data
}

export async function updateLancamento(id: string, payload: Partial<LancamentoDiario>): Promise<LancamentoDiario> {
  const { data } = await api.put<LancamentoDiario>(`/lancamentos/${id}`, payload)
  return data
}

export async function deleteLancamento(id: string): Promise<void> {
  await api.delete(`/lancamentos/${id}`)
}
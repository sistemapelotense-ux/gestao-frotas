import { api } from './api'
import type { ArquivoPropriedade } from '../types'

export async function listArquivoPropriedade(skip = 0, limit = 100): Promise<ArquivoPropriedade[]> {
  const { data } = await api.get<ArquivoPropriedade[]>('/arquivo-propriedade', { params: { skip, limit } })
  return data
}

export async function getArquivoPropriedade(id: string): Promise<ArquivoPropriedade> {
  const { data } = await api.get<ArquivoPropriedade>(`/arquivo-propriedade/${id}`)
  return data
}

export async function createArquivoPropriedade(payload: Partial<ArquivoPropriedade>): Promise<ArquivoPropriedade> {
  const { data } = await api.post<ArquivoPropriedade>('/arquivo-propriedade', payload)
  return data
}

export async function updateArquivoPropriedade(id: string, payload: Partial<ArquivoPropriedade>): Promise<ArquivoPropriedade> {
  const { data } = await api.put<ArquivoPropriedade>(`/arquivo-propriedade/${id}`, payload)
  return data
}

export async function deleteArquivoPropriedade(id: string): Promise<void> {
  await api.delete(`/arquivo-propriedade/${id}`)
}
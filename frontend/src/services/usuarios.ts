import { api } from './api'
import type { Usuario } from '../types'

export async function listUsuarios(skip = 0, limit = 100): Promise<Usuario[]> {
  const { data } = await api.get<Usuario[]>('/usuarios', { params: { skip, limit } })
  return data
}

export async function getUsuario(id: string): Promise<Usuario> {
  const { data } = await api.get<Usuario>(`/usuarios/${id}`)
  return data
}

export async function createUsuario(payload: Partial<Usuario>): Promise<Usuario> {
  const { data } = await api.post<Usuario>('/usuarios', payload)
  return data
}

export async function updateUsuario(id: string, payload: Partial<Usuario>): Promise<Usuario> {
  const { data } = await api.put<Usuario>(`/usuarios/${id}`, payload)
  return data
}

export async function deleteUsuario(id: string): Promise<void> {
  await api.delete(`/usuarios/${id}`)
}
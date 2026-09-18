import { api } from './api'
import type { AuthUser } from '../types'

export interface AuthResponse {
  access_token: string
  token_type: string
}

export async function login(email: string, password: string): Promise<AuthResponse> {
  const { data } = await api.post<AuthResponse>('/auth/token', { email, password })
  localStorage.setItem('access_token', data.access_token)
  return data
}

export async function fetchMe(): Promise<AuthUser> {
  const { data } = await api.get<AuthUser>('/auth/me')
  setCurrentUser(data)
  return data
}

export async function register(
  email: string,
  password: string,
  nome: string,
  papel = 'obra'
): Promise<{ id: string; email: string; nome: string; papel: string }> {
  const { data } = await api.post('/auth/register', { email, password, nome, papel })
  return data
}

export async function changePassword(
  current_password: string,
  new_password: string,
  confirm_password: string
): Promise<void> {
  await api.put('/auth/password', { current_password, new_password, confirm_password })
}

export function getCurrentUser(): AuthUser | null {
  const raw = localStorage.getItem('current_user')
  if (!raw) return null
  try {
    return JSON.parse(raw) as AuthUser
  } catch {
    return null
  }
}

export function setCurrentUser(user: AuthUser): void {
  localStorage.setItem('current_user', JSON.stringify(user))
}

export function logout(): void {
  localStorage.removeItem('access_token')
  localStorage.removeItem('current_user')
}
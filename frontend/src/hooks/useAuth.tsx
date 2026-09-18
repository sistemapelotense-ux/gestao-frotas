import { createContext, useContext, useEffect, useState, ReactNode } from 'react'
import { login as apiLogin, getCurrentUser, logout as apiLogout, register as apiRegister, fetchMe } from '../services/auth'
import type { AuthUser } from '../types'

interface AuthContextType {
  user: AuthUser | null
  token: string | null
  isAuthenticated: boolean
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string, nome: string, papel: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null)
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('access_token'))

  useEffect(() => {
    const u = getCurrentUser()
    if (u) {
      setUser(u)
    } else if (token) {
      fetchMe()
        .then(setUser)
        .catch(() => apiLogout())
    }
  }, [token])

  const login = async (email: string, password: string) => {
    const res = await apiLogin(email, password)
    setToken(res.access_token)
    const me = await fetchMe()
    setUser(me)
  }

  const register = async (email: string, password: string, nome: string, papel: string) => {
    await apiRegister(email, password, nome, papel)
  }

  const logout = () => {
    apiLogout()
    setUser(null)
    setToken(null)
  }

  return (
    <AuthContext.Provider value={{ user, token, isAuthenticated: !!token, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth deve ser usado dentro de AuthProvider')
  return ctx
}
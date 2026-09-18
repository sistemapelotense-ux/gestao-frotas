import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './hooks/useAuth'
import { UIProvider } from './hooks/useUI'
import PrivateRoute from './components/PrivateRoute'
import Layout from './components/layout/Layout'
import Login from './pages/auth/Login'
import Register from './pages/auth/Register'
import Dashboard from './pages/Dashboard'
import Ativos from './pages/Ativos'
import Obras from './pages/Obras'
import Usuarios from './pages/Usuarios'
import Lancamentos from './pages/Lancamentos'
import ArquivoPropriedade from './pages/ArquivoPropriedade'
import Notificacoes from './pages/Notificacoes'
import Consolidacao from './pages/Consolidacao'

export default function App() {
  return (
    <AuthProvider>
      <UIProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            <Route
              path="/"
              element={
                <PrivateRoute>
                  <Layout />
                </PrivateRoute>
              }
            >
              <Route index element={<Navigate to="/dashboard" replace />} />
              <Route path="dashboard" element={<Dashboard />} />
              <Route path="ativos" element={<Ativos />} />
              <Route path="obras" element={<Obras />} />
              <Route path="usuarios" element={<Usuarios />} />
              <Route path="lancamentos" element={<Lancamentos />} />
              <Route path="arquivo-propriedade" element={<ArquivoPropriedade />} />
              <Route path="notificacoes" element={<Notificacoes />} />
              <Route path="consolidacao" element={<Consolidacao />} />
            </Route>

            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BrowserRouter>
      </UIProvider>
    </AuthProvider>
  )
}
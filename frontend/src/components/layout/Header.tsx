import { useAuth } from '../../hooks/useAuth'
import { useNotificacoes } from '../../hooks/useNotificacoes'
import { useNavigate } from 'react-router-dom'

interface HeaderProps {
  onMenuClick: () => void
}

export function Header({ onMenuClick }: HeaderProps) {
  const { user, logout } = useAuth()
  const { naoLidas } = useNotificacoes()
  const navigate = useNavigate()

  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-30">
      <div className="flex items-center justify-between px-4 sm:px-6 py-3">
        <div className="flex items-center gap-3">
          <button
            onClick={onMenuClick}
            className="md:hidden text-gray-500 hover:text-gray-700"
            aria-label="Abrir menu"
          >
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          <div>
            <h2 className="text-lg font-semibold text-gray-900 hidden sm:block">Painel de Controle</h2>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <button
            onClick={() => navigate('/notificacoes')}
            className="relative text-gray-500 hover:text-gray-700"
            aria-label="Notificações"
          >
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
            {naoLidas > 0 && (
              <span className="absolute -top-1 -right-1 h-5 w-5 rounded-full bg-danger-600 text-white text-xs flex items-center justify-center font-bold">
                {naoLidas > 9 ? '9+' : naoLidas}
              </span>
            )}
          </button>

          <span className="badge bg-accent-100 text-accent-700">
            {user?.papel === 'admin' ? 'Administrador' : 'Usuário de Obra'}
          </span>

          <button
            onClick={() => { logout(); navigate('/login') }}
            className="text-gray-500 hover:text-gray-700"
            aria-label="Sair"
          >
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            <span className="hidden sm:inline text-sm ml-1">Sair</span>
          </button>
        </div>
      </div>
    </header>
  )
}
import { NavLink } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import { useNotificacoes } from '../../hooks/useNotificacoes'

interface SidebarProps {
  mobileOpen: boolean
  onClose: () => void
}

const menuItems = [
  { to: '/dashboard', label: 'Dashboard', icon: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' },
  { to: '/lancamentos', label: 'Lançamentos Diários', icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4' },
  { to: '/ativos', label: 'Ativos', icon: 'M12 6v6m0 0l-4-4m4 4l4-4M6 18h12' },
  { to: '/obras', label: 'Obras', icon: 'M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z' },
]

export function Sidebar({ mobileOpen, onClose }: SidebarProps) {
  const { user } = useAuth()
  const { naoLidas } = useNotificacoes()
  const isAdmin = user?.papel === 'admin'

  return (
    <>
      <div className={`fixed inset-0 bg-black/50 z-40 md:hidden ${mobileOpen ? '' : 'hidden'}`} onClick={onClose} />
      <aside className={`fixed inset-y-0 left-0 w-64 bg-navy-900 text-white z-50 flex flex-col transform transition-transform md:transform-none ${mobileOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}`}>
        <div className="px-6 py-5 flex items-center gap-3 border-b border-navy-800">
          <div className="h-10 w-10 bg-accent-600 rounded-lg flex items-center justify-center">
            <svg className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6m0 0l-4-4m4 4l4-4M6 18h12" />
            </svg>
          </div>
          <div>
            <h1 className="font-bold text-sm">Gestão de Ativos</h1>
            <p className="text-xs text-navy-300">Controle de Obras</p>
          </div>
        </div>

        <nav className="flex-1 px-3 py-4 space-y-1">
          {menuItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              onClick={onClose}
              className={({ isActive }) => `flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-accent-600 text-white'
                  : 'text-navy-200 hover:bg-navy-800 hover:text-white'
              }`}
            >
              <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d={item.icon} />
              </svg>
              {item.label}
            </NavLink>
          ))}

          <NavLink
            to="/notificacoes"
            onClick={onClose}
            className={({ isActive }) => `flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
              isActive ? 'bg-accent-600 text-white' : 'text-navy-200 hover:bg-navy-800 hover:text-white'
            }`}
          >
            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
            Notificações
            {naoLidas > 0 && (
              <span className="ml-auto inline-flex items-center justify-center min-w-5 h-5 px-1.5 rounded-full bg-accent-500 text-[11px] font-bold text-white">
                {naoLidas}
              </span>
            )}
          </NavLink>

          {isAdmin && (
            <>
              <NavLink
                to="/usuarios"
                onClick={onClose}
                className={({ isActive }) => `flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  isActive ? 'bg-accent-600 text-white' : 'text-navy-200 hover:bg-navy-800 hover:text-white'
                }`}
              >
                <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                Usuários
              </NavLink>
              <NavLink
                to="/arquivo-propriedade"
                onClick={onClose}
                className={({ isActive }) => `flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  isActive ? 'bg-accent-600 text-white' : 'text-navy-200 hover:bg-navy-800 hover:text-white'
                }`}
              >
                <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M8 7v8a2 2 0 002 2h6M8 7V5a2 2 0 012-2h4.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V15a2 2 0 01-2 2h-2M8 7H6a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2v-2" />
                </svg>
                Arquivo de Propriedade
              </NavLink>
              <NavLink
                to="/consolidacao"
                onClick={onClose}
                className={({ isActive }) => `flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  isActive ? 'bg-accent-600 text-white' : 'text-navy-200 hover:bg-navy-800 hover:text-white'
                }`}
              >
                <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                Consolidação
              </NavLink>
            </>
          )}
        </nav>

        <div className="px-3 py-4 border-t border-navy-800">
          <div className="flex items-center gap-3 px-3">
            <div className="h-9 w-9 bg-accent-600 rounded-full flex items-center justify-center text-sm font-semibold">
              {user?.nome?.charAt(0).toUpperCase() || 'U'}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium truncate">{user?.nome}</p>
              <p className="text-xs text-navy-300 truncate">{user?.email}</p>
            </div>
          </div>
        </div>
      </aside>
    </>
  )
}
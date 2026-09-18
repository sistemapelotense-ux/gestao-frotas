import { useNotificacoes } from '../hooks/useNotificacoes'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'
import EmptyState from '../components/ui/EmptyState'
import Badge from '../components/ui/Badge'

const TIPO_COLORS: Record<string, 'green' | 'yellow' | 'red' | 'blue' | 'violet' | 'gray'> = {
  info: 'blue',
  alerta: 'yellow',
  erro: 'red',
  sucesso: 'green',
}

export default function Notificacoes() {
  const { notificacoes, loading, markRead, markAll } = useNotificacoes()

  const formatDate = (d: string) => {
    try {
      return new Date(d).toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' })
    } catch {
      return d
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <h1 className="text-2xl font-bold text-gray-900">Notificações</h1>
        <Button variant="secondary" onClick={markAll}>Marcar todas como lidas</Button>
      </div>

      <Card>
        {loading ? (
          <div className="text-center py-8 text-gray-500">Carregando...</div>
        ) : notificacoes.length === 0 ? (
          <EmptyState message="Nenhuma notificação" />
        ) : (
          <div className="space-y-3">
            {notificacoes.map((n) => (
              <div
                key={n.id}
                className={`p-4 rounded-xl border transition-colors ${
                  n.lida
                    ? 'bg-white border-gray-100'
                    : 'bg-primary-50/40 border-primary-100'
                }`}
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <Badge color={TIPO_COLORS[n.tipo] || 'gray'}>{n.tipo}</Badge>
                      {!n.lida && <span className="h-2 w-2 rounded-full bg-primary-500" />}
                    </div>
                    <p className="font-medium text-sm text-gray-900">{n.titulo}</p>
                    <p className="text-sm text-gray-600 mt-1">{n.mensagem}</p>
                    <p className="text-xs text-gray-400 mt-2">{formatDate(n.created_at)}</p>
                  </div>
                  {!n.lida && (
                    <button
                      onClick={() => markRead(n.id)}
                      className="text-xs text-primary-600 hover:text-primary-700 whitespace-nowrap"
                    >
                      Marcar lida
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  )
}
import { useEffect, useState } from 'react'
import { useDashboard } from '../hooks/useDashboard'
import { useAuth } from '../hooks/useAuth'
import { useUI } from '../hooks/useUI'
import StatCard from '../components/ui/StatCard'
import Card from '../components/ui/Card'
import Badge from '../components/ui/Badge'
import Table from '../components/ui/Table'
import EmptyState from '../components/ui/EmptyState'
import { getLancamentosRecentes, executarConsolidacao } from '../services/dashboard'
import { handleApiError } from '../services/api'

export default function Dashboard() {
  const { resumo, loading, error } = useDashboard()
  const { user } = useAuth()
  const { showAlert } = useUI()
  const [recentes, setRecentes] = useState<any[]>([])
  const [consolidando, setConsolidando] = useState(false)
  const [resultadoConsolidacao, setResultadoConsolidacao] = useState<any>(null)

  useEffect(() => {
    getLancamentosRecentes()
      .then(setRecentes)
      .catch(() => {})
  }, [])

  const handleConsolidar = async () => {
    setConsolidando(true)
    try {
      const result = await executarConsolidacao()
      setResultadoConsolidacao(result)
    } catch (e) {
      showAlert(handleApiError(e))
    } finally {
      setConsolidando(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-sm text-gray-500 mt-1">Bem-vindo, {user?.nome}</p>
        </div>
        {user?.papel === 'admin' && (
          <button
            onClick={handleConsolidar}
            disabled={consolidando}
            className="btn-accent bg-accent-600 text-white hover:bg-accent-700"
          >
            <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            {consolidando ? 'Consolidando...' : 'Consolidar'}
          </button>
        )}
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-danger-50 text-danger-700 text-sm border border-danger-100">
          {error}
        </div>
      )}

      {loading ? (
        <div className="text-center py-16 text-gray-500">Carregando...</div>
      ) : resumo && (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
            <StatCard
              title="Ativos"
              value={resumo.total_ativos}
              color="primary"
              icon={<svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}><path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6m0 0l-4-4m4 4l4-4" /></svg>}
            />
            <StatCard
              title="Obras"
              value={resumo.total_obras}
              color="violet"
              icon={<svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}><path strokeLinecap="round" strokeLinejoin="round" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>}
            />
            <StatCard
              title="Lançamentos Hoje"
              value={resumo.lancamentos_hoje}
              color="primary"
              icon={<svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}><path strokeLinecap="round" strokeLinejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2" /></svg>}
            />
            <StatCard
              title="Alocados Hoje"
              value={resumo.ativos_alocados_hoje}
              color="success"
              icon={<svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}><path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" /></svg>}
            />
            <StatCard
              title="Não Alocados"
              value={resumo.ativos_nao_alocados}
              color="warning"
              icon={<svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}><path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>}
            />
            <StatCard
              title="Duplicidades"
              value={resumo.duplicidades_hoje}
              color="danger"
              icon={<svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}><path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>}
            />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card title="Ativos não alocados">
              {resumo.detalhe_nao_alocados.length === 0 ? (
                <EmptyState message="Todos os ativos estão alocados" />
              ) : (
                <div className="space-y-2">
                  {resumo.detalhe_nao_alocados.map((item) => (
                    <div key={item.ativo_id} className="flex items-center gap-3 p-2 rounded-lg bg-warning-50 border border-warning-100">
                      <span className="badge-yellow">
                        <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                          <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01" />
                        </svg>
                      </span>
                      <span className="text-sm text-gray-700">{item.identificacao || item.ativo_id}</span>
                    </div>
                  ))}
                </div>
              )}
            </Card>

            <Card title="Duplicidades detectadas">
              {resumo.detalhe_duplicidades.length === 0 ? (
                <EmptyState message="Nenhuma duplicidade encontrada" />
              ) : (
                <div className="space-y-2">
                  {resumo.detalhe_duplicidades.map((item) => (
                    <div key={item.ativo_id} className="p-2 rounded-lg bg-danger-50 border border-danger-100">
                      <p className="text-sm font-medium text-danger-700">Ativo: {item.ativo_id}</p>
                      <p className="text-xs text-gray-600">
                        Obras: {item.obras.join(', ')}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </Card>
          </div>

          {resultadoConsolidacao && (
            <Card title={`Resultado da Consolidação — ${resultadoConsolidacao.periodo?.inicio} a ${resultadoConsolidacao.periodo?.fim}`}>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                <div className="text-center p-4 bg-primary-50 rounded-lg">
                  <p className="text-2xl font-bold text-primary-700">{resultadoConsolidacao.dias_processados}</p>
                  <p className="text-sm text-gray-600">Dias processados</p>
                </div>
                <div className="text-center p-4 bg-warning-50 rounded-lg">
                  <p className="text-2xl font-bold text-warning-700">{resultadoConsolidacao.dias_com_obra_sem_registro?.length || 0}</p>
                  <p className="text-sm text-gray-600">Dias com obras sem registro</p>
                </div>
              </div>
              {resultadoConsolidacao.dias_com_obra_sem_registro?.length > 0 && (
                <div className="mt-4">
                  <p className="text-sm font-medium text-gray-900 mb-2">Obras sem lançamento:</p>
                  {resultadoConsolidacao.dias_com_obra_sem_registro.map((dia: any, i: number) => (
                    <div key={i} className="mb-2 p-3 bg-warning-50 rounded-lg border border-warning-100">
                      <p className="text-sm font-medium text-warning-700">{dia.data}</p>
                      {dia.obras_sem_registro.map((obra: any) => (
                        <p key={obra.id} className="text-xs text-gray-600 ml-2">• {obra.nome}</p>
                      ))}
                    </div>
                  ))}
                </div>
              )}
            </Card>
          )}

          <Card title="Lançamentos recentes">
            {recentes.length === 0 ? (
              <EmptyState message="Nenhum lançamento registrado" />
            ) : (
              <Table headers={['Data', 'Ativo', 'Obra', 'Status']}>
                {recentes.map((l: any) => (
                  <tr key={l.id}>
                    <td>{l.data}</td>
                    <td className="font-medium">{l.ativo}</td>
                    <td>{l.obra}</td>
                    <td>
                      <Badge color={
                        l.status_uso === 'O' ? 'green' :
                        l.status_uso === 'D' ? 'yellow' : 'blue'
                      }>
                        {l.status_uso}
                      </Badge>
                    </td>
                  </tr>
                ))}
              </Table>
            )}
          </Card>
        </>
      )}
    </div>
  )
}
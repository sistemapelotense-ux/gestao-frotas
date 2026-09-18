import { useState } from 'react'
import { executarConsolidacao } from '../services/dashboard'
import { useAuth } from '../hooks/useAuth'
import { useUI } from '../hooks/useUI'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'
import Badge from '../components/ui/Badge'
import { handleApiError } from '../services/api'

export default function Consolidacao() {
  const { user } = useAuth()
  const { showAlert } = useUI()
  const [executando, setExecutando] = useState(false)
  const [resultado, setResultado] = useState<any>(null)

  if (user?.papel !== 'admin') {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <p className="text-gray-500">Acesso restrito a administradores</p>
      </div>
    )
  }

  const handleExecutar = async () => {
    setExecutando(true)
    try {
      const result = await executarConsolidacao()
      setResultado(result)
    } catch (e) {
      showAlert(handleApiError(e))
    } finally {
      setExecutando(false)
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Consolidação de Dados</h1>

      <Card>
        <div className="text-center py-8">
          <div className="mx-auto h-16 w-16 bg-accent-100 rounded-full flex items-center justify-center mb-4">
            <svg className="h-8 w-8 text-accent-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </div>
          <h2 className="text-lg font-semibold text-gray-900 mb-2">Consolidação Automática</h2>
          <p className="text-sm text-gray-500 mb-6 max-w-md mx-auto">
            Compare a lista de ativos da empresa com os lançamentos diários e identifique
            divergências: ativos não alocados e duplicidades.
          </p>
          <Button onClick={handleExecutar} disabled={executando}>
            {executando ? 'Consolidando...' : 'Executar Consolidação'}
          </Button>
        </div>
      </Card>

      {resultado && (
        <Card title={`Resultado — ${resultado.periodo?.inicio} a ${resultado.periodo?.fim}`}>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
            <div className="p-4 bg-primary-50 rounded-lg text-center">
              <p className="text-3xl font-bold text-primary-700">{resultado.dias_processados}</p>
              <p className="text-sm text-gray-600">Dias processados com sucesso</p>
            </div>
            <div className="p-4 bg-warning-50 rounded-lg text-center">
              <p className="text-3xl font-bold text-warning-700">{resultado.dias_com_obra_sem_registro?.length || 0}</p>
              <p className="text-sm text-gray-600">Dias com obras sem registro</p>
            </div>
          </div>

          {resultado.dias_com_obra_sem_registro?.length > 0 && (
            <div className="mb-6">
              <h3 className="text-sm font-semibold text-gray-900 mb-3">Obras sem lançamento:</h3>
              <div className="space-y-2">
                {resultado.dias_com_obra_sem_registro.map((dia: any, i: number) => (
                  <div key={i} className="p-3 bg-warning-50 rounded-lg border border-warning-100">
                    <p className="text-sm font-medium text-warning-700 mb-1">{dia.data}</p>
                    {dia.obras_sem_registro.map((obra: any) => (
                      <p key={obra.id} className="text-xs text-gray-600 ml-3">• {obra.nome}</p>
                    ))}
                  </div>
                ))}
              </div>
            </div>
          )}

          {resultado.detalhes?.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-gray-900 mb-3">Detalhes por dia:</h3>
              <div className="space-y-2">
                {resultado.detalhes.map((dia: any, i: number) => (
                  <div key={i} className="p-3 bg-gray-50 rounded-lg border border-gray-100">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm font-medium text-gray-900">{dia.data}</span>
                      <span className="text-xs text-gray-500">{dia.total_lancamentos} lançamentos</span>
                    </div>
                    {dia.ativos_nao_alocados?.length > 0 && (
                      <Badge color="yellow">
                        {dia.ativos_nao_alocados.length} não alocados
                      </Badge>
                    )}
                    {dia.duplicidades?.length > 0 && (
                      <Badge color="red">
                        {dia.duplicidades.length} duplicidades
                      </Badge>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </Card>
      )}
    </div>
  )
}
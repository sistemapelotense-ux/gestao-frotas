import { useState, useEffect } from 'react'
import { useAuth } from '../hooks/useAuth'
import { useUI } from '../hooks/useUI'
import Table from '../components/ui/Table'
import Card from '../components/ui/Card'
import Modal from '../components/ui/Modal'
import Button from '../components/ui/Button'
import EmptyState from '../components/ui/EmptyState'
import Badge from '../components/ui/Badge'
import { listArquivoPropriedade, createArquivoPropriedade, deleteArquivoPropriedade } from '../services/arquivoPropriedade'
import { listAtivos } from '../services/ativos'
import { handleApiError } from '../services/api'
import type { ArquivoPropriedade, Ativo } from '../types'

const STATUS_LABELS: Record<string, string> = {
  P: 'Próprio',
  L: 'Locado',
  D: 'Disponível',
  C: 'Em manutenção',
}

export default function ArquivoPropriedade() {
  const { user } = useAuth()
  const { showAlert, showConfirm } = useUI()
  const isAdmin = user?.papel === 'admin'
  const [itens, setItens] = useState<ArquivoPropriedade[]>([])
  const [ativos, setAtivos] = useState<Ativo[]>([])
  const [loading, setLoading] = useState(false)
  const [showModal, setShowModal] = useState(false)
  const [statusFilter, setStatusFilter] = useState('')
  const [selectedAtivo, setSelectedAtivo] = useState('')
  const [selectedStatus, setSelectedStatus] = useState('P')

  const loadData = async () => {
    setLoading(true)
    try {
      const [i, a] = await Promise.all([
        listArquivoPropriedade(),
        listAtivos(),
      ])
      setItens(i)
      setAtivos(a)
    } catch (e) {
      showAlert(handleApiError(e))
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { loadData() }, [])

  const getAtivoInfo = (ativoId: string) => ativos.find((a) => a.id === ativoId)

  const filtered = statusFilter
    ? itens.filter((i) => i.status === statusFilter)
    : itens

  const handleCreate = async () => {
    try {
      await createArquivoPropriedade({ ativo_id: selectedAtivo, status: selectedStatus })
      setShowModal(false)
      await loadData()
    } catch (e) {
      showAlert(handleApiError(e))
    }
  }

  const handleDelete = async (id: string) => {
    showConfirm('Tem certeza?', async () => {
      await deleteArquivoPropriedade(id)
      await loadData()
    })
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <h1 className="text-2xl font-bold text-gray-900">Arquivo de Propriedade</h1>
        {isAdmin && (
          <Button onClick={() => setShowModal(true)}>+ Adicionar Ativo</Button>
        )}
      </div>

      <Card>
        <div className="mb-4 flex flex-col sm:flex-row gap-3">
          <select className="input" value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
            <option value="">Todos os status</option>
            {Object.entries(STATUS_LABELS).map(([k, v]) => (
              <option key={k} value={k}>{v}</option>
            ))}
          </select>
        </div>

        {loading ? (
          <div className="text-center py-8 text-gray-500">Carregando...</div>
        ) : filtered.length === 0 ? (
          <EmptyState message="Nenhum item no arquivo de propriedade" />
        ) : (
          <Table headers={['Identificação', 'Descrição', 'Fabricante', 'Modelo', 'Status', 'Ações']}>
            {filtered.map((item) => {
              const ativo = getAtivoInfo(item.ativo_id)
              return (
                <tr key={item.id}>
                  <td className="font-medium">{ativo?.identificacao || '-'}</td>
                  <td>{ativo?.descricao || '-'}</td>
                  <td>{ativo?.fabricante || '-'}</td>
                  <td>{ativo?.modelo || '-'}</td>
                  <td>
                    <Badge color={
                      item.status === 'P' ? 'blue' :
                      item.status === 'L' ? 'yellow' :
                      item.status === 'D' ? 'gray' :
                      'red'
                    }>
                      {STATUS_LABELS[item.status] || item.status}
                    </Badge>
                  </td>
                  {isAdmin && (
                    <td>
                      <button onClick={() => handleDelete(item.id)} className="text-danger-600 hover:text-danger-700 text-sm">
                        Excluir
                      </button>
                    </td>
                  )}
                </tr>
              )
            })}
          </Table>
        )}
      </Card>

      <Modal open={showModal} onClose={() => setShowModal(false)} title="Adicionar ao Arquivo de Propriedade">
        <div className="space-y-4">
          <div>
            <label className="label">Ativo *</label>
            <select className="input" value={selectedAtivo} onChange={(e) => setSelectedAtivo(e.target.value)} required>
              <option value="">Selecione...</option>
              {ativos.map((a) => (
                <option key={a.id} value={a.id}>{a.identificacao} - {a.descricao}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="label">Status *</label>
            <select className="input" value={selectedStatus} onChange={(e) => setSelectedStatus(e.target.value)} required>
              {Object.entries(STATUS_LABELS).map(([k, v]) => (
                <option key={k} value={k}>{v}</option>
              ))}
            </select>
          </div>
          <div className="flex justify-end gap-3 pt-4">
            <Button variant="secondary" onClick={() => setShowModal(false)}>Cancelar</Button>
            <Button onClick={handleCreate}>Adicionar</Button>
          </div>
        </div>
      </Modal>
    </div>
  )
}
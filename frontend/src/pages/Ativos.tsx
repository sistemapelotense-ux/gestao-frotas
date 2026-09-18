import { useState } from 'react'
import { useAtivos } from '../hooks/useAtivos'
import { useAuth } from '../hooks/useAuth'
import { useUI } from '../hooks/useUI'
import Table from '../components/ui/Table'
import Card from '../components/ui/Card'
import Modal from '../components/ui/Modal'
import Button from '../components/ui/Button'
import Input from '../components/ui/Input'
import EmptyState from '../components/ui/EmptyState'
import Badge from '../components/ui/Badge'
import { handleApiError } from '../services/api'
import type { Ativo } from '../types'

export default function Ativos() {
  const { user } = useAuth()
  const { showAlert, showConfirm } = useUI()
  const isAdmin = user?.papel === 'admin'
  const [search, setSearch] = useState('')
  const { ativos, loading, create, update, remove } = useAtivos(search || undefined)
  const [showModal, setShowModal] = useState(false)
  const [editId, setEditId] = useState<string | null>(null)
  const [form, setForm] = useState<Partial<Ativo>>({})

  const handleNew = () => {
    setEditId(null)
    setForm({ identificacao: '', descricao: '', tipo: '', fabricante: '', modelo: '' })
    setShowModal(true)
  }

  const handleEdit = (a: Ativo) => {
    setEditId(a.id)
    setForm({ ...a })
    setShowModal(true)
  }

  const handleSave = async () => {
    try {
      if (editId) {
        await update(editId, form)
      } else {
        await create(form)
      }
      setShowModal(false)
    } catch (e) {
      showAlert(handleApiError(e))
    }
  }

  const handleDelete = async (id: string) => {
    showConfirm('Tem certeza que deseja excluir este ativo?', async () => {
      await remove(id)
    })
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <h1 className="text-2xl font-bold text-gray-900">Ativos</h1>
        {isAdmin && (
          <Button onClick={handleNew}>
            + Novo Ativo
          </Button>
        )}
      </div>

      <Card>
        <div className="mb-4">
          <input
            type="text"
            placeholder="Buscar por identificação, tipo, fabricante..."
            className="input"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        {loading ? (
          <div className="text-center py-8 text-gray-500">Carregando...</div>
        ) : ativos.length === 0 ? (
          <EmptyState message="Nenhum ativo cadastrado" />
        ) : (
          <Table headers={['Identificação', 'Descrição', 'Tipo', 'Fabricante', 'Modelo', 'Status', 'Ações']}>
            {ativos.map((a) => (
              <tr key={a.id}>
                <td className="font-medium">{a.identificacao}</td>
                <td>{a.descricao}</td>
                <td>{a.tipo}</td>
                <td>{a.fabricante}</td>
                <td>{a.modelo}</td>
                <td>
                  <Badge color={a.status === 'disponivel' ? 'green' : a.status === 'locado' ? 'yellow' : 'gray'}>
                    {a.status}
                  </Badge>
                </td>
                {isAdmin && (
                  <td>
                    <button onClick={() => handleEdit(a)} className="text-primary-600 hover:text-primary-700 text-sm mr-2">
                      Editar
                    </button>
                    <button onClick={() => handleDelete(a.id)} className="text-danger-600 hover:text-danger-700 text-sm">
                      Excluir
                    </button>
                  </td>
                )}
              </tr>
            ))}
          </Table>
        )}
      </Card>

      <Modal open={showModal} onClose={() => setShowModal(false)} title={editId ? 'Editar Ativo' : 'Novo Ativo'}>
        <div className="space-y-4">
          <Input label="Identificação *" value={form.identificacao || ''} onChange={(v) => setForm({ ...form, identificacao: v })} required />
          <Input label="Descrição" value={form.descricao || ''} onChange={(v) => setForm({ ...form, descricao: v })} />
          <Input label="Tipo" value={form.tipo || ''} onChange={(v) => setForm({ ...form, tipo: v })} />
          <Input label="Fabricante" value={form.fabricante || ''} onChange={(v) => setForm({ ...form, fabricante: v })} />
          <Input label="Modelo" value={form.modelo || ''} onChange={(v) => setForm({ ...form, modelo: v })} />
          <div className="flex justify-end gap-3 pt-4">
            <Button variant="secondary" onClick={() => setShowModal(false)}>Cancelar</Button>
            <Button onClick={handleSave}>Salvar</Button>
          </div>
        </div>
      </Modal>
    </div>
  )
}
import { useState } from 'react'
import { useObras } from '../hooks/useObras'
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
import type { Obra } from '../types'

export default function Obras() {
  const { user } = useAuth()
  const { showAlert, showConfirm } = useUI()
  const isAdmin = user?.papel === 'admin'
  const [search, setSearch] = useState('')
  const { obras, loading, create, update, remove } = useObras(search || undefined)
  const [showModal, setShowModal] = useState(false)
  const [editId, setEditId] = useState<string | null>(null)
  const [form, setForm] = useState<Partial<Obra>>({})

  const handleNew = () => {
    setEditId(null)
    setForm({ nome: '', localizacao: '' })
    setShowModal(true)
  }

  const handleEdit = (o: Obra) => {
    setEditId(o.id)
    setForm({ ...o })
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
    showConfirm('Tem certeza que deseja excluir esta obra?', async () => {
      await remove(id)
    })
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <h1 className="text-2xl font-bold text-gray-900">Obras</h1>
        {isAdmin && (
          <Button onClick={handleNew}>+ Nova Obra</Button>
        )}
      </div>

      <Card>
        <div className="mb-4">
          <input
            type="text"
            placeholder="Buscar por nome ou localização..."
            className="input"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        {loading ? (
          <div className="text-center py-8 text-gray-500">Carregando...</div>
        ) : obras.length === 0 ? (
          <EmptyState message="Nenhuma obra cadastrada" />
        ) : (
          <Table headers={['Nome', 'Localização', 'Status', 'Ações']}>
            {obras.map((o) => (
              <tr key={o.id}>
                <td className="font-medium">{o.nome}</td>
                <td>{o.localizacao}</td>
                <td>
                  <Badge color={o.ativa ? 'green' : 'gray'}>
                    {o.ativa ? 'Ativa' : 'Inativa'}
                  </Badge>
                </td>
                {isAdmin && (
                  <td>
                    <button onClick={() => handleEdit(o)} className="text-primary-600 hover:text-primary-700 text-sm mr-2">
                      Editar
                    </button>
                    <button onClick={() => handleDelete(o.id)} className="text-danger-600 hover:text-danger-700 text-sm">
                      Excluir
                    </button>
                  </td>
                )}
              </tr>
            ))}
          </Table>
        )}
      </Card>

      <Modal open={showModal} onClose={() => setShowModal(false)} title={editId ? 'Editar Obra' : 'Nova Obra'}>
        <div className="space-y-4">
          <Input label="Nome *" value={form.nome || ''} onChange={(v) => setForm({ ...form, nome: v })} required />
          <Input label="Localização *" value={form.localizacao || ''} onChange={(v) => setForm({ ...form, localizacao: v })} required />
          <div className="flex justify-end gap-3 pt-4">
            <Button variant="secondary" onClick={() => setShowModal(false)}>Cancelar</Button>
            <Button onClick={handleSave}>Salvar</Button>
          </div>
        </div>
      </Modal>
    </div>
  )
}
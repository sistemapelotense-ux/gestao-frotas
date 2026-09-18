import { useState } from 'react'
import { useUsuarios } from '../hooks/useUsuarios'
import { useObras } from '../hooks/useObras'
import { useUI } from '../hooks/useUI'
import Table from '../components/ui/Table'
import Card from '../components/ui/Card'
import Modal from '../components/ui/Modal'
import Button from '../components/ui/Button'
import Input from '../components/ui/Input'
import EmptyState from '../components/ui/EmptyState'
import Badge from '../components/ui/Badge'
import { handleApiError } from '../services/api'
import type { Usuario } from '../types'

export default function Usuarios() {
  const { showAlert, showConfirm } = useUI()
  const { usuarios, loading, create, update, remove } = useUsuarios()
  const { obras } = useObras()
  const [showModal, setShowModal] = useState(false)
  const [editId, setEditId] = useState<string | null>(null)
  const [form, setForm] = useState<any>({})

  const getObraNome = (id: string | null) => {
    if (!id) return '-'
    const obra = obras.find((o) => o.id === id)
    return obra?.nome || '-'
  }

  const handleNew = () => {
    setEditId(null)
    setForm({ email: '', password: '', nome: '', papel: 'obra', obra_id: '' })
    setShowModal(true)
  }

  const handleEdit = (u: Usuario) => {
    setEditId(u.id)
    setForm({ ...u, password: '' })
    setShowModal(true)
  }

  const handleSave = async () => {
    try {
      if (editId) {
        const payload: any = { ...form }
        delete payload.password
        if (form.password) payload.password = form.password
        await update(editId, payload)
      } else {
        await create(form)
      }
      setShowModal(false)
    } catch (e) {
      showAlert(handleApiError(e))
    }
  }

  const handleDelete = async (id: string) => {
    showConfirm('Tem certeza que deseja excluir este usuário?', async () => {
      await remove(id)
    })
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <h1 className="text-2xl font-bold text-gray-900">Usuários</h1>
        <Button onClick={handleNew}>+ Novo Usuário</Button>
      </div>

      <Card>
        {loading ? (
          <div className="text-center py-8 text-gray-500">Carregando...</div>
        ) : usuarios.length === 0 ? (
          <EmptyState message="Nenhum usuário cadastrado" />
        ) : (
          <Table headers={['Nome', 'E-mail', 'Papel', 'Obra', 'Status', 'Ações']}>
            {usuarios.map((u) => (
              <tr key={u.id}>
                <td className="font-medium">{u.nome}</td>
                <td>{u.email}</td>
                <td>
                  <Badge color={u.papel === 'admin' ? 'violet' : 'blue'}>
                    {u.papel === 'admin' ? 'Administrador' : 'Obra'}
                  </Badge>
                </td>
                <td>{getObraNome(u.obra_id)}</td>
                <td>
                  <Badge color={u.ativo ? 'green' : 'gray'}>
                    {u.ativo ? 'Ativo' : 'Inativo'}
                  </Badge>
                </td>
                <td>
                  <button onClick={() => handleEdit(u)} className="text-primary-600 hover:text-primary-700 text-sm mr-2">
                    Editar
                  </button>
                  <button onClick={() => handleDelete(u.id)} className="text-danger-600 hover:text-danger-700 text-sm">
                    {u.ativo ? 'Desativar' : 'Ativar'}
                  </button>
                </td>
              </tr>
            ))}
          </Table>
        )}
      </Card>

      <Modal open={showModal} onClose={() => setShowModal(false)} title={editId ? 'Editar Usuário' : 'Novo Usuário'}>
        <div className="space-y-4">
          <Input label="Nome *" value={form.nome || ''} onChange={(v) => setForm({ ...form, nome: v })} required />
          <Input label="E-mail *" type="email" value={form.email || ''} onChange={(v) => setForm({ ...form, email: v })} required />
          {!editId && (
            <Input label="Senha *" type="password" value={form.password || ''} onChange={(v) => setForm({ ...form, password: v })} required />
          )}
          {editId && form.password !== undefined && (
            <Input label="Nova senha (deixe vazio para manter)" type="password" value={form.password || ''} onChange={(v) => setForm({ ...form, password: v })} />
          )}
          <Input
            label="Papel"
            value={form.papel || 'obra'}
            onChange={(v) => setForm({ ...form, papel: v })}
            selectOptions={['admin', 'obra']}
          />
          <div>
            <label className="label">Obra vinculada</label>
            <select
              className="input"
              value={form.obra_id || ''}
              onChange={(e) => setForm({ ...form, obra_id: e.target.value || null })}
            >
              <option value="">Nenhuma obra</option>
              {obras.map((o) => (
                <option key={o.id} value={o.id}>{o.nome}</option>
              ))}
            </select>
          </div>
          <div className="flex justify-end gap-3 pt-4">
            <Button variant="secondary" onClick={() => setShowModal(false)}>Cancelar</Button>
            <Button onClick={handleSave}>Salvar</Button>
          </div>
        </div>
      </Modal>
    </div>
  )
}
import { useState } from 'react'
import { useLancamentos } from '../hooks/useLancamentos'
import { useAtivos } from '../hooks/useAtivos'
import { useObras } from '../hooks/useObras'
import { useAuth } from '../hooks/useAuth'
import { useUI } from '../hooks/useUI'
import Card from '../components/ui/Card'
import Modal from '../components/ui/Modal'
import Button from '../components/ui/Button'
import Input from '../components/ui/Input'
import EmptyState from '../components/ui/EmptyState'
import Badge from '../components/ui/Badge'
import { handleApiError } from '../services/api'
import type { LancamentoDiario } from '../types'

const STATUS_OPTIONS = ['O', 'D', 'P', 'C', 'R']
const CLIMA_OPTIONS = ['Ensolarado', 'Nublado', 'Chuvoso', 'Parcialmente nublado', 'Neblina']
const STATUS_LABELS: Record<string, string> = { O: 'Operando', D: 'Disponível', P: 'Parado', C: 'Em manutenção', R: 'Reserva' }

export default function Lancamentos() {
  const { user } = useAuth()
  const { showAlert, showConfirm } = useUI()
  const { lancamentos, loading, create, update, remove } = useLancamentos()
  const { ativos } = useAtivos()
  const { obras } = useObras()
  const [showModal, setShowModal] = useState(false)
  const [editId, setEditId] = useState<string | null>(null)
  const [form, setForm] = useState<any>({})

  const getAtivo = (id: string) => ativos.find((a) => a.id === id)
  const getObra = (id: string) => obras.find((o) => o.id === id)

  const formatDate = (d: string) => {
    try {
      return new Date(d).toLocaleDateString('pt-BR')
    } catch {
      return d
    }
  }

  const handleNew = () => {
    setEditId(null)
    setForm({
      data: new Date().toISOString().split('T')[0],
      ativo_id: '',
      obra_id: user?.obra_id || '',
      status_uso: '',
      informacoes_dia: '',
      codigo_ativo: '',
      descricao: '',
      tipo: '',
      fabricante: '',
      modelo: '',
      horimetro_inicial: 0,
      horimetro_final: 0,
      km_inicial: 0,
      km_final: 0,
      descritivo_manutencao: '',
      status: 'pendente',
      condicao_climatica: '',
    })
    setShowModal(true)
  }

  const handleEdit = (l: LancamentoDiario) => {
    setEditId(l.id)
    setForm({ ...l, data: l.data.split('T')[0] })
    setShowModal(true)
  }

  const handleAtivoSelect = (ativoId: string) => {
    const ativo = ativos.find((a) => a.id === ativoId)
    setForm({
      ...form,
      ativo_id: ativoId,
      codigo_ativo: ativo?.identificacao || '',
      descricao: ativo?.descricao || '',
      tipo: ativo?.tipo || '',
      fabricante: ativo?.fabricante || '',
      modelo: ativo?.modelo || '',
    })
  }

  const handleSave = async () => {
    try {
      const payload = {
        ...form,
        data: form.data + 'T12:00:00',
        total_horas: (parseFloat(form.horimetro_final) || 0) - (parseFloat(form.horimetro_inicial) || 0),
        total_km: (parseFloat(form.km_final) || 0) - (parseFloat(form.km_inicial) || 0),
      }
      if (editId) {
        await update(editId, payload)
      } else {
        await create(payload)
      }
      setShowModal(false)
    } catch (e) {
      showAlert(handleApiError(e))
    }
  }

  const handleDelete = async (id: string) => {
    showConfirm('Tem certeza que deseja excluir este lançamento?', async () => {
      await remove(id)
    })
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <h1 className="text-2xl font-bold text-gray-900">Lançamentos Diários</h1>
        <Button onClick={handleNew}>+ Novo Lançamento</Button>
      </div>

      <Card>
        {loading ? (
          <div className="text-center py-8 text-gray-500">Carregando...</div>
        ) : lancamentos.length === 0 ? (
          <EmptyState message="Nenhum lançamento registrado" />
        ) : (
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>Data</th>
                  <th>Ativo</th>
                  <th>Obra</th>
                  <th>Status Uso</th>
                  <th>Hórimetro</th>
                  <th>KM</th>
                  <th>Status</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {lancamentos.map((l) => (
                  <tr key={l.id}>
                    <td>{formatDate(l.data)}</td>
                    <td className="font-medium">{l.codigo_ativo || getAtivo(l.ativo_id)?.identificacao || '-'}</td>
                    <td>{getObra(l.obra_id)?.nome || '-'}</td>
                    <td>
                      <Badge color={
                        l.status_uso === 'O' ? 'green' :
                        l.status_uso === 'D' ? 'yellow' :
                        l.status_uso === 'C' ? 'red' : 'blue'
                      }>
                        {STATUS_LABELS[l.status_uso] || l.status_uso}
                      </Badge>
                    </td>
                    <td>{l.horimetro_inicial.toFixed(1)} → {l.horimetro_final.toFixed(1)}</td>
                    <td>{l.km_inicial.toFixed(0)} → {l.km_final.toFixed(0)}</td>
                    <td>
                      <Badge color={l.status === 'pendente' ? 'yellow' : 'green'}>
                        {l.status}
                      </Badge>
                    </td>
                    <td>
                      <button onClick={() => handleEdit(l)} className="text-primary-600 hover:text-primary-700 text-sm mr-2">
                        Editar
                      </button>
                      <button onClick={() => handleDelete(l.id)} className="text-danger-600 hover:text-danger-700 text-sm">
                        Excluir
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>

      <Modal open={showModal} onClose={() => setShowModal(false)} title={editId ? 'Editar Lançamento' : 'Novo Lançamento'}>
        <div className="space-y-4 max-h-[60vh] overflow-y-auto pr-2">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <Input label="Data *" type="date" value={form.data || ''} onChange={(v) => setForm({ ...form, data: v })} required />
            <Input label="Status de Uso *" value={form.status_uso || ''} onChange={(v) => setForm({ ...form, status_uso: v })} selectOptions={STATUS_OPTIONS} required />
          </div>
          <div>
            <label className="label">Ativo *</label>
            <select className="input" value={form.ativo_id || ''} onChange={(e) => handleAtivoSelect(e.target.value)} required>
              <option value="">Selecione o ativo...</option>
              {ativos.map((a) => (
                <option key={a.id} value={a.id}>{a.identificacao} - {a.descricao}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="label">Obra *</label>
            <select className="input" value={form.obra_id || ''} onChange={(e) => setForm({ ...form, obra_id: e.target.value })} required>
              <option value="">Selecione a obra...</option>
              {obras.map((o) => (
                <option key={o.id} value={o.id}>{o.nome}</option>
              ))}
            </select>
          </div>
          <Input label="Informações do dia *" value={form.informacoes_dia || ''} onChange={(v) => setForm({ ...form, informacoes_dia: v })} required />
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <Input label="Código do Ativo *" value={form.codigo_ativo || ''} onChange={(v) => setForm({ ...form, codigo_ativo: v })} required />
            <Input label="Condição Climática *" value={form.condicao_climatica || ''} onChange={(v) => setForm({ ...form, condicao_climatica: v })} selectOptions={CLIMA_OPTIONS} required />
          </div>
          <Input label="Descrição *" value={form.descricao || ''} onChange={(v) => setForm({ ...form, descricao: v })} required />
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <Input label="Tipo *" value={form.tipo || ''} onChange={(v) => setForm({ ...form, tipo: v })} required />
            <Input label="Fabricante *" value={form.fabricante || ''} onChange={(v) => setForm({ ...form, fabricante: v })} required />
            <Input label="Modelo *" value={form.modelo || ''} onChange={(v) => setForm({ ...form, modelo: v })} required />
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <Input label="Horímetro Inicial *" type="number" value={form.horimetro_inicial || 0} onChange={(v) => setForm({ ...form, horimetro_inicial: v })} required />
            <Input label="Horímetro Final *" type="number" value={form.horimetro_final || 0} onChange={(v) => setForm({ ...form, horimetro_final: v })} required />
            <Input label="KM Inicial *" type="number" value={form.km_inicial || 0} onChange={(v) => setForm({ ...form, km_inicial: v })} required />
            <Input label="KM Final *" type="number" value={form.km_final || 0} onChange={(v) => setForm({ ...form, km_final: v })} required />
          </div>
          <Input label="Status *" value={form.status || 'pendente'} onChange={(v) => setForm({ ...form, status: v })} selectOptions={['pendente', 'concluido']} required />
          <div>
            <label className="label">Descritivo de Manutenção e Outros</label>
            <textarea
              className="input"
              rows={3}
              value={form.descritivo_manutencao || ''}
              onChange={(e) => setForm({ ...form, descritivo_manutencao: e.target.value })}
              placeholder="Campo opcional"
            />
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
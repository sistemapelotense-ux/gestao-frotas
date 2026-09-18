import { api } from './api'
import type { DashboardResumo, LancamentoDiario } from '../types'

export async function getDashboardResumo(): Promise<DashboardResumo> {
  const { data } = await api.get<DashboardResumo>('/dashboard')
  return data
}

export async function getLancamentosRecentes(): Promise<LancamentoDiario[]> {
  const { data } = await api.get<LancamentoDiario[]>('/dashboard/lancamentos-recentes')
  return data
}

export async function executarConsolidacao(): Promise<unknown> {
  const { data } = await api.post('/consolidacao/executar')
  return data
}
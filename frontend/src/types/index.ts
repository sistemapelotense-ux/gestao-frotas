export interface Ativo {
  id: string
  identificacao: string
  descricao: string
  tipo: string
  fabricante: string
  modelo: string
  status: string
  created_at: string
  updated_at: string
}

export interface Obra {
  id: string
  nome: string
  localizacao: string
  ativa: boolean
  created_at: string
  updated_at: string
}

export interface Usuario {
  id: string
  email: string
  nome: string
  papel: string
  obra_id: string | null
  ativo: boolean
  created_at: string
  updated_at: string
}

export interface LancamentoDiario {
  id: string
  data: string
  ativo_id: string
  obra_id: string
  usuario_id: string
  status_uso: string
  informacoes_dia: string
  codigo_ativo: string
  descricao: string
  tipo: string
  fabricante: string
  modelo: string
  horimetro_inicial: number
  horimetro_final: number
  total_horas: number
  km_inicial: number
  km_final: number
  total_km: number
  descritivo_manutencao: string | null
  status: string
  condicao_climatica: string
  created_at: string
  updated_at: string
}

export interface ArquivoPropriedade {
  id: string
  ativo_id: string
  status: string
  created_at: string
  updated_at: string
}

export interface Notificacao {
  id: string
  titulo: string
  mensagem: string
  lida: boolean
  tipo: string
  created_at: string
}

export interface DashboardResumo {
  total_ativos: number
  total_obras: number
  lancamentos_hoje: number
  ativos_alocados_hoje: number
  ativos_nao_alocados: number
  duplicidades_hoje: number
  detalhe_nao_alocados: Array<{ ativo_id: string, identificacao: string }>
  detalhe_duplicidades: Array<{ ativo_id: string, obras: string[] }>
}

export interface AuthUser {
  id: string
  email: string
  nome: string
  papel: string
  obra_id: string | null
}
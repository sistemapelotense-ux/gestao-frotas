import { createContext, useContext, useState, ReactNode } from 'react'
import Modal from '../components/ui/Modal'
import Button from '../components/ui/Button'

interface UIContextType {
  showAlert: (message: string, title?: string) => void
  showConfirm: (message: string, onConfirm: () => void, title?: string) => void
}

const UIContext = createContext<UIContextType | null>(null)

interface State {
  kind: 'alert' | 'confirm'
  title: string
  message: string
  onConfirm?: () => void
}

export function UIProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<State | null>(null)

  const showAlert = (message: string, title = 'Aviso') => {
    setState({ kind: 'alert', title, message })
  }

  const showConfirm = (message: string, onConfirm: () => void, title = 'Confirmação') => {
    setState({ kind: 'confirm', title, message, onConfirm })
  }

  const close = () => setState(null)

  return (
    <UIContext.Provider value={{ showAlert, showConfirm }}>
      {children}

      <Modal open={state !== null} onClose={close} title={state?.title || ''}>
        <p className="text-sm text-gray-600 mb-6">{state?.message}</p>
        <div className="flex justify-end gap-3">
          {state?.kind === 'confirm' && (
            <Button variant="secondary" onClick={close}>Cancelar</Button>
          )}
          <Button
            variant={state?.kind === 'confirm' ? 'danger' : 'primary'}
            onClick={() => {
              if (state?.kind === 'confirm' && state?.onConfirm) {
                state.onConfirm()
              }
              close()
            }}
          >
            {state?.kind === 'confirm' ? 'Confirmar' : 'OK'}
          </Button>
        </div>
      </Modal>
    </UIContext.Provider>
  )
}

export function useUI() {
  const ctx = useContext(UIContext)
  if (!ctx) throw new Error('useUI deve ser usado dentro de UIProvider')
  return ctx
}
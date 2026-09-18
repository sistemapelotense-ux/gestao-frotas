interface InputProps {
  label?: string
  value: string | number
  onChange: (value: string) => void
  type?: string
  placeholder?: string
  required?: boolean
  name?: string
  selectOptions?: string[]
}

export default function Input({
  label,
  value,
  onChange,
  type = 'text',
  placeholder,
  required,
  name,
  selectOptions,
}: InputProps) {
  if (selectOptions) {
    return (
      <div>
        {label && <label className="label" htmlFor={name}>{label}{required && <span className="text-danger-500"> *</span>}</label>}
        <select
          id={name}
          name={name}
          className="input"
          value={String(value)}
          onChange={(e) => onChange(e.target.value)}
          required={required}
        >
          <option value="">Selecione...</option>
          {selectOptions.map((opt) => (
            <option key={opt} value={opt}>{opt}</option>
          ))}
        </select>
      </div>
    )
  }
  return (
    <div>
      {label && <label className="label" htmlFor={name}>{label}{required && <span className="text-danger-500"> *</span>}</label>}
      <input
        id={name}
        name={name}
        type={type}
        className="input"
        value={value}
        placeholder={placeholder}
        onChange={(e) => onChange(e.target.value)}
        required={required}
      />
    </div>
  )
}
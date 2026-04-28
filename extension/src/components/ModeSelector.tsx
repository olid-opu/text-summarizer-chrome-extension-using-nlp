import type { SummaryType } from "../lib/api";

interface Props {
  value: SummaryType;
  onChange: (v: SummaryType) => void;
  disabled?: boolean;
}

const OPTIONS: { value: SummaryType; label: string }[] = [
  { value: "short", label: "Short" },
  { value: "medium", label: "Medium" },
  { value: "detailed", label: "Detailed" },
];

export default function ModeSelector({ value, onChange, disabled }: Props) {
  return (
    <div className="card">
      <span className="label">Summary length</span>
      <div className="segmented" role="tablist">
        {OPTIONS.map((opt) => (
          <button
            key={opt.value}
            type="button"
            role="tab"
            aria-selected={value === opt.value}
            className={value === opt.value ? "active" : ""}
            onClick={() => onChange(opt.value)}
            disabled={disabled}
          >
            {opt.label}
          </button>
        ))}
      </div>
    </div>
  );
}
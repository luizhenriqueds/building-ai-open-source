type Props = { label: string; value: number };

export function RatingMeter({ label, value }: Props) {
  return (
    <div className="grid grid-cols-[6.5rem_minmax(0,1fr)_2.5rem] items-center gap-3 text-sm">
      <span className="text-muted-foreground">{label}</span>
      <div
        role="meter"
        aria-label={label}
        aria-valuemin={0}
        aria-valuemax={10}
        aria-valuenow={value}
        className="h-2 overflow-hidden rounded-full bg-input"
      >
        <div
          className="h-full bg-primary"
          style={{ width: `${value * 10}%` }}
        />
      </div>
      <span className="text-right font-mono">{value}/10</span>
    </div>
  );
}

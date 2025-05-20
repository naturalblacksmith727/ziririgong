export default function RangeSlider({ label, min, max, value, onChange }) {
  return (
    <div className="flex items-center gap-2">
      <label className="w-15">{label}</label>
      <input
        type="range"
        min={min}
        max={max}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className="mx-2"
      />
      <span className="w-10 text-right">{value}</span>
    </div>
  );
}

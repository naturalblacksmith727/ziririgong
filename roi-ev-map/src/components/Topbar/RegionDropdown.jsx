export default function RegionDropdown({ value, onChange, options }) {
  return (
    <label>
      지역:&nbsp;
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="ml-1"
      >
        {options.map((opt) => (
          <option key={opt} value={opt}>
            {opt}
          </option>
        ))}
      </select>
    </label>
  );
}

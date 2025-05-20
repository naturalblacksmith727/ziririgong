export default function YearDropdown({ value, onChange, options }) {
  return (
    <label>
      연도:&nbsp;
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="ml-1"
      >
        {options.map((opt) => (
          <option key={opt} value={opt}>
            {opt === "전체" ? "전체" : `${opt}년`}
          </option>
        ))}
      </select>
    </label>
  );
}

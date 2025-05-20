export default function SortOption({ sortBy, setSortBy, sortOpts }) {
  return (
    <label>
      <strong>정렬 기준:&nbsp;</strong>
      <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
        {sortOpts.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
    </label>
  );
}

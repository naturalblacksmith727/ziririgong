import SortOption from "./SortOption";
import RankingList from "./RankingList";
import * as turf from "@turf/turf";

export default function RankingSection({
  features,
  sortBy,
  setSortBy,
  sortOpts,
  setSelectedCenter,
}) {
  return (
    <div className="w-76 p-4 bg-white rounded-2xl shadow">
      {/* 정렬 기준 드롭다운 */}
      <div className="mb-6">
        <SortOption sortBy={sortBy} setSortBy={setSortBy} sortOpts={sortOpts} />
      </div>
      {/* <label>
        <strong>정렬 기준:&nbsp;</strong>
        <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
          {sortOpts.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </label> */}
      {/* 순위 리스트 */}
      <ol>
        {features.slice(0, 10).map((f, i) => {
          // 1) turf.js로 중심좌표 계산
          const centroid = turf.centroid(f); // f는 GeoJSON Feature
          const [lon, lat] = centroid.geometry.coordinates;

          return (
            <li
              key={f.properties.ADM_CD}
              onClick={() => setSelectedCenter([lon, lat])}
              style={{ cursor: "pointer" }}
              className="hover:bg-gray-100 transition"
            >
              {i + 1}. {f.properties.ADM_NM}{" "}
            </li>
          );
        })}
      </ol>
      {/* <RankingList features={features.slice(0, 10)} /> 상위 10개 표시 */}
    </div>
  );
}

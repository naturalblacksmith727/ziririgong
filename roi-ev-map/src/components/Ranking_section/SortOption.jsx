import { useState } from "react";

export default function SortOption() {
  const [sort, setSort] = useState("주차장수");

  return (
    <div className="mb-2">
      <span className="font-semibold mr-2">정렬 기준:</span>
      <label className="mr-3">
        <input
          type="radio"
          value="주차장수"
          checked={sort === "주차장수"}
          onChange={(e) => setSort(e.target.value)}
        />
        공용 주차장 수
      </label>
      <label className="mr-3">
        <input
          type="radio"
          value="구획수"
          checked={sort === "구획수"}
          onChange={(e) => setSort(e.target.value)}
        />
        주차장 구획 수
      </label>
      <label>
        <input
          type="radio"
          value="충전기수"
          checked={sort === "충전기수"}
          onChange={(e) => setSort(e.target.value)}
        />
        충전기 수
      </label>
    </div>
  );
}

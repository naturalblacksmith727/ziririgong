import { useState, useEffect } from "react";
import Topbar from "./components/Topbar/Topbar";
import MapDisplay from "./components/MapDisplay";
import RankingSection from "./components/Ranking_section/RankingSection";

/* ───── 지역·타입·연도 값은 GeoJSON 값과 ‘완전히 동일’하게 작성 ───── */
const REGION_OPTS = ["전체", "서울", "경기", "인천"];
const YEAR_OPTS = ["전체", "2021", "2026", "2030"];
const SORT_OPTS = [
  { value: "pub_parking_cnt_desc", label: "공영주차장 많은 순" },
  { value: "pub_parking_ev_asc", label: "공영주차장에 있는 충전기 수 적은 순" },
  { value: "pub_parking_section_desc", label: "공영주차장 구획 수 많은 순" },
  { value: "pri_parking_ev_asc", label: "민영주차장에 있는 충전기 수 적은 순" },
];

export default function App() {
  const [geo, setGeo] = useState(null);

  /* 모든 UI가 공유하는 전역 필터·정렬 state */
  const [ui, setUI] = useState({
    region: "전체",
    year: "전체",
    minTraffic: 0, // ← 이동량 슬라이더 값
    minStation: 0, // ← 충전소 수 슬라이더 값
    sortBy: "pub_parking_cnt_desc",
  });

  const [selectedCenter, setSelectedCenter] = useState(null);

  /* GeoJSON 1회만 로드 */
  useEffect(() => {
    fetch("/metro_roi_region.geojson")
      .then((res) => res.json())
      .then((data) => {
        console.log("geojson 데이터", data);
        setGeo(data);
      })
      .catch((err) => console.error("GeoJSON load error:", err));
  }, []);

  if (!geo) return <p>로딩 중...</p>;

  // console.log("Geo", geo);
  /* 필터링 */
  const filtered = geo
    ? geo.features.filter((f) => {
        const region = ui.region;
        const p = f.properties;
        return (
          (region === "전체" || p.region === region) &&
          p.traffic >= ui.minTraffic &&
          p.station_cnt <= ui.minStation
        );
      })
    : [];
  // console.log("filtered", filtered);

  /* 정렬 */
  const sorted = [...filtered].sort((a, b) => {
    const p = ui.sortBy;
    if (p === "pub_parking_cnt_desc")
      return b.properties.pub_parking_cnt - a.properties.pub_parking_cnt;
    if (p === "pub_parking_ev_asc")
      return a.properties.pub_parking_ev_cnt - b.properties.pub_parking_ev_cnt;
    if (p === "pub_parking_section_desc")
      return (
        b.properties.pub_parking_section_cnt -
        a.properties.pub_parking_section_cnt
      );
    if (p === "pri_parking_ev_asc")
      return a.properties.pri_parking_ev_cnt - b.properties.pri_parking_ev_cnt;
    // 혹시나 예외(기본값) 처리
    return 0;
  });

  const maxTraffic = Math.max(...geo.features.map((f) => f.properties.traffic));
  const maxStation = Math.max(
    ...geo.features.map((f) => f.properties.station_cnt)
  );

  return (
    <div className="min-h-screen bg-gray-50 flex-col">
      <div className="ml-16 mt-10">
        <Topbar
          ui={ui}
          setUI={setUI}
          regionOpts={REGION_OPTS}
          yearOpts={YEAR_OPTS}
          maxTraffic={maxTraffic}
          maxStation={maxStation}
        />
      </div>
      <div className="flex gap-8">
        {/* 지도는 필터링만 반영 */}
        <div className="rounded-xl w-[900px] h-[400px] ml-32 mb-8">
          <MapDisplay features={filtered} selectedCenter={selectedCenter} />
        </div>
        {/* 순위는 필터 + 정렬 반영 */}
        <div className="mr-12 mt-4">
          <RankingSection
            features={sorted}
            sortBy={ui.sortBy}
            setSortBy={(sortBy) => setUI((u) => ({ ...u, sortBy }))}
            sortOpts={SORT_OPTS}
            setSelectedCenter={setSelectedCenter}
          />
        </div>
      </div>
    </div>
  );
}
// function App() {
//   return (
//     <div className="min-h-screen bg-gray-50 font-sans">
//       {/* 상단 TopBar: (좌측정렬, 여백 plenty) */}
//       <div
//         className="w-full flex justify-start px-14 py-8 bg-white shadow"
//         style={{ fontFamily: "Pretendard, sans-serif" }}
//       >
//         <Topbar />
//       </div>
//       {/* 본문: 지도+순위 */}
//       <div className="flex flex-row justify-start items-start gap-8 px-14 pt-10">
//         {/* 지도 */}
//         <div
//           className="rounded-2xl shadow-lg overflow-hidden bg-white"
//           style={{ width: "800px", height: "550px" }}
//         >
//           <MapDisplay />
//         </div>
//         {/* 우측 순위 */}
//         <div className="w-72 p-6 bg-white rounded-2xl shadow flex flex-col items-start border border-gray-200">d
//           <RankingSection />
//         </div>
//       </div>
//     </div>
//   );
// }

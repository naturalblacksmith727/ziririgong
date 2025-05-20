import RegionDropdown from "./RegionDropdown";
import YearDropdown from "./YearDropdown";
import RangeSlider from "./RangeSlider";

export default function Topbar({
  maxTraffic,
  maxStation,
  ui,
  setUI,
  regionOpts,
  yearOpts,
}) {
  return (
    <div className="flex items-center gap-14 p-6 bg-blue-100">
      <RegionDropdown
        value={ui.region}
        options={regionOpts}
        onChange={(val) => setUI((u) => ({ ...u, region: val }))}
      />

      <YearDropdown
        value={ui.year}
        options={yearOpts}
        onChange={(val) => setUI((u) => ({ ...u, year: val }))}
      />

      <RangeSlider
        label="이동량"
        value={ui.minTraffic}
        min={0}
        max={maxTraffic}
        onChange={(val) => setUI((u) => ({ ...u, minTraffic: val }))}
      />

      <RangeSlider
        label="충전소수"
        value={ui.minStation}
        min={0}
        max={maxStation}
        onChange={(val) => setUI((u) => ({ ...u, minStation: val }))}
      />
    </div>
  );
  // // 상태 선언
  // const [year, setYear] = useState("2021");
  // const [region, setRegion] = useState("서울특별시");
  // const [moveRange, setMoveRange] = useState(0); // 이동량 슬라이더
  // const [chargerRange, setChargerRange] = useState(0); // 충전소 수 슬라이더

  // // 옵션은 일단 하드코딩 (실제 데이터 확정 시 교체)
  // const yearOptions = ["2021", "2026", "2030"];
  // const regionOptions = ["서울특별시", "경기도", "인천광역시"];

  // return (
  //   <div className="flex gap-4 items-center justify-center mb-4">
  //     {/* 드롭다운 2개 */}
  //     <select
  //       value={year}
  //       onChange={(e) => setYear(e.target.value)}
  //       className="border rounded px-2 py-1"
  //     >
  //       <option value="2021">2021년</option>
  //       <option value="2026">2026년</option>
  //       <option value="2030">2030년</option>
  //     </select>
  //     <select
  //       value={region}
  //       onChange={(e) => setRegion(e.target.value)}
  //       className="border rounded px-2 py-1"
  //     >
  //       <option value="서울특별시">서울특별시</option>
  //       <option value="경기도">경기도</option>
  //       <option value="인천광역시">인천광역시</option>
  //     </select>

  //     {/* 슬라이더 2개 */}
  //     <div className="flex flex-col items-center">
  //       <label htmlFor="moveRange">이동량: {moveRange}</label>
  //       <input
  //         id="moveRange"
  //         type="range"
  //         min={0}
  //         max={1000}
  //         value={moveRange}
  //         onChange={(e) => setMoveRange(Number(e.target.value))}
  //         className="w-32"
  //       />
  //     </div>
  //     <div className="flex flex-col items-center">
  //       <label htmlFor="chargerRange">충전소 수: {chargerRange}</label>
  //       <input
  //         id="chargerRange"
  //         type="range"
  //         min={0}
  //         max={100}
  //         value={chargerRange}
  //         onChange={(e) => setChargerRange(Number(e.target.value))}
  //         className="w-32"
  //       />
  //     </div>
  //   </div>
  // );
}

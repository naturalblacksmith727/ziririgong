import Topbar from "./components/Topbar/Topbar";
import MapDisplay from "./components/MapDisplay";
import RankingSection from "./components/Ranking_section/RankingSection";

function App() {
  return (
    <div className="min-h-screen bg-gray-50 font-sans">
      {/* 상단 TopBar: (좌측정렬, 여백 plenty) */}
      <div
        className="w-full flex justify-start px-14 py-8 bg-white shadow"
        style={{ fontFamily: "Pretendard, sans-serif" }}
      >
        <Topbar />
      </div>
      {/* 본문: 지도+순위 */}
      <div className="flex flex-row justify-start items-start gap-8 px-14 pt-10">
        {/* 지도 */}
        <div
          className="rounded-2xl shadow-lg overflow-hidden bg-white"
          style={{ width: "800px", height: "550px" }}
        >
          <MapDisplay />
        </div>
        {/* 우측 순위 */}
        <div className="w-72 p-6 bg-white rounded-2xl shadow flex flex-col items-start border border-gray-200">
          <RankingSection />
        </div>
      </div>
    </div>
  );
}

// function App() {
//   return (
//     <div className="h-screen w-screen flex items-end justify-start">
//       <div className="p-8">
//         <div
//           className="rounded-2xl shadow-lg overflow-hidden"
//           style={{ width: "900px", height: "600px" }}
//         >
//           <MapDisplay />
//         </div>
//       </div>
//     </div>
//   );
// }

export default App;

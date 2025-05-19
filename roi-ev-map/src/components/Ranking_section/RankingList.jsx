export default function RankingList() {
  // 더미 데이터
  const dummyList = [
    { rank: 1, name: "강남구", value: 120 },
    { rank: 2, name: "송파구", value: 110 },
    { rank: 3, name: "서초구", value: 105 },
    { rank: 4, name: "영등포구", value: 97 },
  ];

  return (
    <div>
      <span className="font-semibold mb-2">순위 리스트</span>
      <ul className="mt-2">
        {dummyList.map((item) => (
          <li key={item.rank} className="mb-1">
            {item.rank}. {item.name} ({item.value})
          </li>
        ))}
      </ul>
    </div>
  );
}

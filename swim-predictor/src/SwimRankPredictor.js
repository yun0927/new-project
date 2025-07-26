import React, { useState } from 'react';

export default function SwimRankPredictor() {
  const [event, setEvent] = useState('');
  const [age, setAge] = useState('');
  const [predictedRank, setPredictedRank] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // 사용자 입력 (기록) 받는 상태
  const [userTime, setUserTime] = useState(''); // 예: "0:32'75" 혹은 초단위 입력도 가능

  // API 호출 + 순위 계산
  const handlePredict = async () => {
    setError('');
    setPredictedRank(null);

    if (!event || !age || !userTime) {
      setError('모든 값을 입력해주세요.');
      return;
    }

    setLoading(true);
    try {
      // FastAPI에서 전체 데이터 가져오기 (필터 없이)
      const res = await fetch('http://127.0.0.1:8000/swim_rank');
      const data = await res.json();

      // 조건에 맞는 데이터 필터링
      const filtered = data.filter(
        (item) => item.event === event && item.age === age
      );

      // 사용자의 time을 초 단위 숫자로 변환 (간단하게 'time_sec' 입력 받는 게 편할 수도)
      // 여기서는 초단위 입력 받는 걸로 가정
      const userTimeSec = parseFloat(userTime);

      if (isNaN(userTimeSec)) {
        setError('기록을 초 단위 숫자로 입력해주세요.');
        setLoading(false);
        return;
      }

      // 순위 계산: 사용자의 기록보다 빠른 기록이 몇 개 있는지 세기 + 1
      const rank = filtered.filter((item) => item.time_sec < userTimeSec).length + 1;

      setPredictedRank(rank);
    } catch (e) {
      setError('데이터를 가져오는 데 실패했습니다.');
    }
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 400, margin: 'auto' }}>
      <h2>수영 순위 예측기</h2>

      <div>
        <label>
          이벤트 (event):{' '}
          <input
            type="text"
            value={event}
            onChange={(e) => setEvent(e.target.value)}
            placeholder="예: freestyle"
          />
        </label>
      </div>

      <div>
        <label>
          연령대 (age):{' '}
          <input
            type="text"
            value={age}
            onChange={(e) => setAge(e.target.value)}
            placeholder="예: 20-24"
          />
        </label>
      </div>

      <div>
        <label>
          기록 (초 단위):{' '}
          <input
            type="text"
            value={userTime}
            onChange={(e) => setUserTime(e.target.value)}
            placeholder="예: 32.75"
          />
        </label>
      </div>

      <button onClick={handlePredict} disabled={loading}>
        {loading ? '예측 중...' : '순위 예측하기'}
      </button>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {predictedRank !== null && (
        <p>예상 순위는 <strong>{predictedRank} 위</strong> 입니다.</p>
      )}
    </div>
  );
}

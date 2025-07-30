import React, { useState } from 'react';

function SwimRankPredictor() {
  const [gender, setGender] = useState('M');
  const [age, setAge] = useState('20-24');
  const [event, setEvent] = useState('freestyle');
  const [timeSec, setTimeSec] = useState('');
  const [rank, setRank] = useState(null);
  const [error, setError] = useState(null);

  const handlePredict = async () => {
    if (!timeSec) {
      setError('기록(초)을 입력해주세요.');
      return;
    }

    const params = new URLSearchParams({
      gender,
      age,
      event,
      time_sec: timeSec,  // 문자열이라도 FastAPI에서 float로 변환 가능
    });

    try {
      const response = await fetch(`http://127.0.0.1:8000/predict_rank?${params}`);
      if (!response.ok) throw new Error('API 요청 실패');
      const data = await response.json();
      console.log('API 응답 데이터:', data); // 디버깅용
      setRank(data.predicted_rank);           // 여기 수정됨
      setError(null);
    } catch (err) {
      setError('순위 예측에 실패했습니다.');
      setRank(null);
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: 'auto', padding: 20 }}>
      <h2>🏊‍♂️ 수영 순위 예측기</h2>

      <div>
        <label>성별: </label>
        <select value={gender} onChange={e => setGender(e.target.value)}>
          <option value="M">남자 (M)</option>
          <option value="F">여자 (F)</option>
        </select>
      </div>

      <div>
        <label>연령대: </label>
        <select value={age} onChange={e => setAge(e.target.value)}>
          <option value="20-24">20-24</option>
          <option value="25-29">25-29</option>
          <option value="30-34">30-34</option>
          {/* 필요한 연령대 추가 가능 */}
        </select>
      </div>

      <div>
        <label>종목: </label>
        <select value={event} onChange={e => setEvent(e.target.value)}>
          <option value="freestyle">freestyle</option>
          <option value="Back">Back</option>
          <option value="Breast">Breast</option>
          <option value="Fly">Fly</option>
        </select>
      </div>

      <div>
        <label>기록 (초): </label>
        <input
          type="number"
          value={timeSec}
          onChange={e => setTimeSec(e.target.value)}
          placeholder="예: 32.45"
          step="0.01"
          min="0"
        />
      </div>

      <button onClick={handlePredict} style={{ marginTop: 10 }}>
        순위 예측
      </button>

      {rank !== null && (
        <div style={{ marginTop: 20 }}>
          🏅 예상 순위: <strong>{rank} 위</strong>
        </div>
      )}

      {error && (
        <div style={{ marginTop: 20, color: 'red' }}>
          ⚠️ {error}
        </div>
      )}
    </div>
  );
}

export default SwimRankPredictor;

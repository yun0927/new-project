import React, { useState } from "react";

function App() {
  const [gender, setGender] = useState("M");
  const [age, setAge] = useState("20-24");
  const [event, setEvent] = useState("freestyle");
  const [record, setRecord] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      const response = await fetch("http://localhost:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ gender, age, event, record: parseFloat(record) }),
      });

      const data = await response.json();

      if (response.ok) {
        setResult(data);
      } else {
        setError(data.message || "예측 실패");
        setResult(null);
      }
    } catch (err) {
      setError("서버 연결 실패");
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>🏊 내 수영 순위 예측</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>성별:</label>
          <select value={gender} onChange={(e) => setGender(e.target.value)}>
            <option value="M">남</option>
            <option value="F">여</option>
          </select>
        </div>
        <div>
          <label>나이대:</label>
          <select value={age} onChange={(e) => setAge(e.target.value)}>
            <option value="20-24">20-24</option>
            <option value="25-29">25-29</option>
            <option value="30-34">30-34</option>
            {/* 필요시 더 추가 */}
          </select>
        </div>
        <div>
          <label>종목:</label>
          <select value={event} onChange={(e) => setEvent(e.target.value)}>
            <option value="freestyle">자유형</option>
            <option value="backstroke">배영</option>
            {/* 종목은 CSV 기준으로 */}
          </select>
        </div>
        <div>
          <label>기록 (초):</label>
          <input
            type="number"
            step="0.01"
            value={record}
            onChange={(e) => setRecord(e.target.value)}
            required
          />
        </div>
        <button type="submit">예측하기</button>
      </form>

      {result && (
        <div style={{ marginTop: "1rem" }}>
          <h2>🏅 결과</h2>
          <p>예상 순위: {result.predicted_rank}위</p>
          <p>전체 참가자 수: {result.total_participants}명</p>
        </div>
      )}

      {error && (
        <div style={{ marginTop: "1rem", color: "red" }}>
          <strong>에러: {error}</strong>
        </div>
      )}
    </div>
  );
}

export default App;


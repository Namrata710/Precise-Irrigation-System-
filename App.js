import React, { useState } from 'react';

function App() {
  const [status, setStatus] = useState("");

  const checkIrrigation = async () => {
    const res = await fetch('http://127.0.0.1:5000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ soil_moisture: 20 })
    });
    const data = await res.json();
    setStatus(data.irrigation);
  };

  return (
    <div>
      <h1>Irrigation System</h1>
      <button onClick={checkIrrigation}>Check</button>
      <p>Status: {status}</p>
    </div>
  );
}

export default App;

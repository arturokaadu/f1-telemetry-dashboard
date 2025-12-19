import React, { useState, useEffect } from 'react';
import axios from 'axios';
import DriverComparison from './components/DriverComparison';
import './App.css';

function App() {
  const [sessions, setSessions] = useState([]);
  const [selectedSession, setSelectedSession] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Fetch available sessions
    fetchSessions();
  }, []);

  const fetchSessions = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/sessions');
      setSessions(response.data.sessions);
    } catch (error) {
      console.error('Error fetching sessions:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🏎️ F1 Telemetry Dashboard</h1>
        <p>Monaco 2024 Analysis</p>
      </header>

      <main className="container">
        <DriverComparison sessionId={selectedSession} />
      </main>

      <footer>
        <p>Built by Arturo Kaadú with Luna</p>
      </footer>
    </div>
  );
}

export default App;

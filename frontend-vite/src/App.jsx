import React, { useState, useEffect } from 'react';
import axios from 'axios';
import styled from 'styled-components';
import DriverComparison from './components/DriverComparison.jsx';
import RacePaceOverview from './components/RacePaceOverview.jsx';
import TireDegradation from './components/TireDegradation.jsx';
import TrackStatus from './components/TrackStatus.jsx';

const AppContainer = styled.div`
  background: linear-gradient(135deg, #15151E 0%, #1A1A2E 100%);
  min-height: 100vh;
  color: #FFFFFF;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  padding: 40px 20px;
`;

const Header = styled.header`
  text-align: center;
  margin-bottom: 60px;
`;

const Title = styled.h1`
  font-size: 4rem;
  font-weight: 700;
  letter-spacing: 8px;
  margin: 0;
  text-transform: uppercase;
  background: linear-gradient(90deg, #FFFFFF 0%, #E10600 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  
  @media (max-width: 768px) {
    font-size: 2.5rem;
    letter-spacing: 4px;
  }
`;

const Subtitle = styled.p`
  font-size: 1.1rem;
  font-weight: 200;
  color: rgba(255, 255, 255, 0.6);
  margin-top: 10px;
  letter-spacing: 2px;
`;

const Container = styled.div`
  max-width: 1400px;
  margin: 0 auto;
`;

const StatusCard = styled.div`
  background: rgba(30, 30, 46, 0.6);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 40px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
`;

const StatusText = styled.p`
  margin: 0;
  font-size: 0.9rem;
  font-weight: 300;
  color: rgba(255, 255, 255, 0.8);
  
  strong {
    color: #E10600;
    font-weight: 500;
  }
`;

const Footer = styled.footer`
  text-align: center;
  margin-top: 80px;
  padding: 40px 20px;
  color: rgba(255, 255, 255, 0.4);
  font-weight: 200;
  font-size: 0.9rem;
`;

const RedAccent = styled.span`
  color: #E10600;
`;

const DashboardGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 32px;
  margin-bottom: 40px;

  @media (max-width: 1200px) {
    grid-template-columns: 1fr;
  }
`;

function App() {
  const [sessions, setSessions] = useState([]);
  const [selectedSession, setSelectedSession] = useState('monaco_2024'); // Default to Monaco 2024
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Load Google Fonts - Inter (modern sans-serif)
    const link = document.createElement('link');
    link.href = 'https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500;700&display=swap';
    link.rel = 'stylesheet';
    document.head.appendChild(link);

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
    <AppContainer>
      <Container>
        <Header>
          <Title>F1 TELEMETRY</Title>
          <Subtitle>Monaco 2024 Analysis</Subtitle>
        </Header>

        <StatusCard>
          <StatusText>
            <strong>System Status:</strong> All systems operational | ML models active
          </StatusText>
        </StatusCard>

        <DashboardGrid>
          <TrackStatus />
          <RacePaceOverview />
        </DashboardGrid>

        <DashboardGrid>
          <DriverComparison sessionId={selectedSession} />
          <TireDegradation />
        </DashboardGrid>

        <Footer>
          Built by Arturo Kaadú with <RedAccent>Luna</RedAccent> 💙
        </Footer>
      </Container>
    </AppContainer>
  );
}

export default App;

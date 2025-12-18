import React from 'react';
import styled from 'styled-components';

const StatusCard = styled.div`
  background: rgba(30, 30, 46, 0.6);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  transition: transform 0.3s ease, box-shadow 0.3s ease;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 48px rgba(225, 6, 0, 0.2);
  }
`;

const SectionTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 300;
  letter-spacing: 2px;
  margin: 0 0 24px 0;
  color: #FFFFFF;
  text-transform: uppercase;
`;

const StatusGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
`;

const StatusItem = styled.div`
  background: rgba(20, 20, 30, 0.6);
  padding: 16px;
  border-radius: 8px;
  border-left: 3px solid ${props => props.color || '#00D2BE'};
`;

const StatusLabel = styled.div`
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 1px;
`;

const StatusValue = styled.div`
  font-size: 1.4rem;
  font-weight: 500;
  color: #FFFFFF;
`;

const LiveIndicator = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
`;

const LiveDot = styled.div`
  width: 10px;
  height: 10px;
  background: #00FF00;
  border-radius: 50%;
  animation: pulse 2s infinite;

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
  }
`;

const LiveText = styled.span`
  color: #00FF00;
  font-size: 0.9rem;
  font-weight: 500;
  letter-spacing: 1px;
  text-transform: uppercase;
`;

function TrackStatus() {
  return (
    <StatusCard>
      <SectionTitle>Track Status</SectionTitle>

      <LiveIndicator>
        <LiveDot />
        <LiveText>Live Session</LiveText>
      </LiveIndicator>

      <StatusGrid>
        <StatusItem color="#E10600">
          <StatusLabel>Session</StatusLabel>
          <StatusValue>Race</StatusValue>
        </StatusItem>

        <StatusItem color="#00D2BE">
          <StatusLabel>Circuit</StatusLabel>
          <StatusValue>Monaco</StatusValue>
        </StatusItem>

        <StatusItem color="#FFD700">
          <StatusLabel>Weather</StatusLabel>
          <StatusValue>☀️ Sunny</StatusValue>
        </StatusItem>

        <StatusItem color="#FF8C00">
          <StatusLabel>Track Temp</StatusLabel>
          <StatusValue>52°C</StatusValue>
        </StatusItem>

        <StatusItem color="#0600EF">
          <StatusLabel>Air Temp</StatusLabel>
          <StatusValue>28°C</StatusValue>
        </StatusItem>

        <StatusItem color="#00FF00">
          <StatusLabel>Track Status</StatusLabel>
          <StatusValue>🟢 Green</StatusValue>
        </StatusItem>
      </StatusGrid>
    </StatusCard>
  );
}

export default TrackStatus;

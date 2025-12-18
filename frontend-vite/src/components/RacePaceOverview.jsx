import React from 'react';
import styled from 'styled-components';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const PaceCard = styled.div`
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

const PaceGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
`;

const PaceStat = styled.div`
  background: rgba(20, 20, 30, 0.6);
  padding: 16px;
  border-radius: 8px;
  border-left: 3px solid ${props => props.color || '#E10600'};
`;

const StatLabel = styled.div`
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 1px;
`;

const StatValue = styled.div`
  font-size: 1.8rem;
  font-weight: 500;
  color: #FFFFFF;
  font-family: 'Courier New', monospace;
`;

function RacePaceOverview({ sessionData }) {
    // Mock data for demonstration
    const paceData = [
        { driver: 'VER', avgLapTime: 74.23, fastestLap: 73.65 },
        { driver: 'HAM', avgLapTime: 74.89, fastestLap: 74.43 },
        { driver: 'LEC', avgLapTime: 75.12, fastestLap: 74.87 },
        { driver: 'PER', avgLapTime: 75.45, fastestLap: 75.01 },
    ];

    const chartData = paceData.map(d => ({
        name: d.driver,
        'Avg Lap': d.avgLapTime,
        'Fastest': d.fastestLap
    }));

    return (
        <PaceCard>
            <SectionTitle>Race Pace Overview</SectionTitle>

            <PaceGrid>
                {paceData.map(driver => (
                    <PaceStat key={driver.driver} color={driver.driver === 'VER' ? '#0600EF' : driver.driver === 'HAM' ? '#00D2BE' : '#E10600'}>
                        <StatLabel>{driver.driver} - Avg Pace</StatLabel>
                        <StatValue>{driver.avgLapTime.toFixed(3)}s</StatValue>
                    </PaceStat>
                ))}
            </PaceGrid>

            <ResponsiveContainer width="100%" height={250}>
                <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.1)" />
                    <XAxis dataKey="name" stroke="rgba(255, 255, 255, 0.5)" />
                    <YAxis stroke="rgba(255, 255, 255, 0.5)" domain={[73, 76]} />
                    <Tooltip
                        contentStyle={{
                            background: 'rgba(20, 20, 30, 0.95)',
                            border: '1px solid rgba(255, 255, 255, 0.2)',
                            borderRadius: '8px',
                            color: '#FFFFFF'
                        }}
                    />
                    <Legend />
                    <Bar dataKey="Avg Lap" fill="#E10600" />
                    <Bar dataKey="Fastest" fill="#00D2BE" />
                </BarChart>
            </ResponsiveContainer>
        </PaceCard>
    );
}

export default RacePaceOverview;

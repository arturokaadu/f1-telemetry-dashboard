import React from 'react';
import styled from 'styled-components';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const TireCard = styled.div`
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

const TireInfo = styled.div`
  display: flex;
  gap: 20px;
  margin-bottom: 24px;
  flex-wrap: wrap;
`;

const TireBadge = styled.div`
  background: ${props => props.color || 'rgba(255, 255, 255, 0.1)'};
  padding: 12px 24px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 12px;
`;

const TireLabel = styled.span`
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 300;
`;

const TireValue = styled.span`
  font-size: 1.1rem;
  color: #FFFFFF;
  font-weight: 500;
`;

function TireDegradation() {
    // Mock tire degradation data
    const tireData = [
        { lap: 1, degradation: 0, lapTime: 74.5 },
        { lap: 2, degradation: 2, lapTime: 74.6 },
        { lap: 3, degradation: 4, lapTime: 74.8 },
        { lap: 4, degradation: 6, lapTime: 75.0 },
        { lap: 5, degradation: 9, lapTime: 75.3 },
        { lap: 6, degradation: 12, lapTime: 75.7 },
        { lap: 7, degradation: 15, lapTime: 76.1 },
        { lap: 8, degradation: 19, lapTime: 76.6 },
        { lap: 9, degradation: 23, lapTime: 77.2 },
        { lap: 10, degradation: 28, lapTime: 77.9 },
    ];

    return (
        <TireCard>
            <SectionTitle>Tire Degradation Analysis</SectionTitle>

            <TireInfo>
                <TireBadge color="rgba(255, 50, 50, 0.3)">
                    <TireLabel>Compound:</TireLabel>
                    <TireValue>SOFT</TireValue>
                </TireBadge>
                <TireBadge color="rgba(225, 6, 0, 0.2)">
                    <TireLabel>Tire Age:</TireLabel>
                    <TireValue>10 laps</TireValue>
                </TireBadge>
                <TireBadge color="rgba(255, 150, 0, 0.2)">
                    <TireLabel>Degradation:</TireLabel>
                    <TireValue>28%</TireValue>
                </TireBadge>
            </TireInfo>

            <ResponsiveContainer width="100%" height={280}>
                <LineChart data={tireData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.1)" />
                    <XAxis
                        dataKey="lap"
                        stroke="rgba(255, 255, 255, 0.5)"
                        label={{ value: 'Lap Number', position: 'insideBottom', offset: -5, fill: 'rgba(255, 255, 255, 0.6)' }}
                    />
                    <YAxis
                        stroke="rgba(255, 255, 255, 0.5)"
                        label={{ value: 'Degradation %', angle: -90, position: 'insideLeft', fill: 'rgba(255, 255, 255, 0.6)' }}
                    />
                    <Tooltip
                        contentStyle={{
                            background: 'rgba(20, 20, 30, 0.95)',
                            border: '1px solid rgba(255, 255, 255, 0.2)',
                            borderRadius: '8px',
                            color: '#FFFFFF'
                        }}
                    />
                    <Legend />
                    <Line
                        type="monotone"
                        dataKey="degradation"
                        stroke="#FF3333"
                        strokeWidth={3}
                        dot={{ fill: '#FF3333', r: 5 }}
                        name="Tire Degradation %"
                    />
                </LineChart>
            </ResponsiveContainer>
        </TireCard>
    );
}

export default TireDegradation;

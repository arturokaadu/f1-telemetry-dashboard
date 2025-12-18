import React, { useState, useEffect } from 'react';
import axios from 'axios';
import styled from 'styled-components';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const ComparisonContainer = styled.div`
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

const SectionTitle = styled.h2`
  font-size: 1.8rem;
  font-weight: 300;
  letter-spacing: 2px;
  margin: 0 0 32px 0;
  color: #FFFFFF;
  text-transform: uppercase;
`;

const DriverSelectors = styled.div`
  display: flex;
  align-items: center;
  gap: 24px;
  margin-bottom: 40px;
  flex-wrap: wrap;
`;

const Select = styled.select`
  background: rgba(20, 20, 30, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: #FFFFFF;
  padding: 12px 20px;
  font-size: 1rem;
  font-weight: 300;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 200px;

  &:hover {
    border-color: #E10600;
    box-shadow: 0 0 20px rgba(225, 6, 0, 0.2);
  }

  &:focus {
    outline: none;
    border-color: #E10600;
  }

  option {
    background: #1A1A2E;
    color: #FFFFFF;
  }
`;

const VsText = styled.span`
  font-size: 1.2rem;
  font-weight: 200;
  color: rgba(255, 255, 255, 0.5);
  letter-spacing: 2px;
`;

const LoadingText = styled.p`
  text-align: center;
  font-size: 1.1rem;
  font-weight: 200;
  color: rgba(255, 255, 255, 0.6);
  padding: 60px 0;
`;

function DriverComparison({ sessionId }) {
    const [driver1, setDriver1] = useState('VER');
    const [driver2, setDriver2] = useState('HAM');
    const [lapData, setLapData] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (sessionId) {
            fetchComparisonData();
        }
    }, [driver1, driver2, sessionId]);

    const fetchComparisonData = async () => {
        setLoading(true);
        try {
            const response = await axios.post('http://localhost:5000/api/compare', {
                driver1,
                driver2,
                session_id: sessionId
            });
            setLapData(response.data.comparison);
        } catch (error) {
            console.error('Error fetching comparison:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <ComparisonContainer>
            <SectionTitle>Driver Comparison</SectionTitle>

            <DriverSelectors>
                <Select value={driver1} onChange={(e) => setDriver1(e.target.value)}>
                    <option value="VER">Max Verstappen</option>
                    <option value="HAM">Lewis Hamilton</option>
                    <option value="LEC">Charles Leclerc</option>
                    <option value="PER">Sergio Perez</option>
                </Select>

                <VsText>VS</VsText>

                <Select value={driver2} onChange={(e) => setDriver2(e.target.value)}>
                    <option value="HAM">Lewis Hamilton</option>
                    <option value="VER">Max Verstappen</option>
                    <option value="LEC">Charles Leclerc</option>
                    <option value="PER">Sergio Perez</option>
                </Select>
            </DriverSelectors>

            {loading ? (
                <LoadingText>Loading telemetry data...</LoadingText>
            ) : (
                <ResponsiveContainer width="100%" height={400}>
                    <LineChart data={lapData}>
                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.1)" />
                        <XAxis
                            dataKey="lap"
                            stroke="rgba(255, 255, 255, 0.5)"
                            label={{ value: 'Lap Number', position: 'insideBottom', offset: -5, fill: 'rgba(255, 255, 255, 0.6)' }}
                        />
                        <YAxis
                            stroke="rgba(255, 255, 255, 0.5)"
                            label={{ value: 'Lap Time (s)', angle: -90, position: 'insideLeft', fill: 'rgba(255, 255, 255, 0.6)' }}
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
                            dataKey="driver1Time"
                            stroke="#0090FF"
                            strokeWidth={2}
                            dot={{ fill: '#0090FF', r: 4 }}
                            name={driver1}
                        />
                        <Line
                            type="monotone"
                            dataKey="driver2Time"
                            stroke="#00E0AC"
                            strokeWidth={2}
                            dot={{ fill: '#00E0AC', r: 4 }}
                            name={driver2}
                        />
                    </LineChart>
                </ResponsiveContainer>
            )}
        </ComparisonContainer>
    );
}

export default DriverComparison;

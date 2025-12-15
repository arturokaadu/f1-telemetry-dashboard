import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

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
        <div className="driver-comparison">
            <h2>Driver Comparison</h2>

            <div className="driver-selectors">
                <select value={driver1} onChange={(e) => setDriver1(e.target.value)}>
                    <option value="VER">Max Verstappen</option>
                    <option value="HAM">Lewis Hamilton</option>
                    <option value="LEC">Charles Leclerc</option>
                    <option value="PER">Sergio Perez</option>
                </select>

                <span>vs</span>

                <select value={driver2} onChange={(e) => setDriver2(e.target.value)}>
                    <option value="HAM">Lewis Hamilton</option>
                    <option value="VER">Max Verstappen</option>
                    <option value="LEC">Charles Leclerc</option>
                    <option value="PER">Sergio Perez</option>
                </select>
            </div>

            {loading ? (
                <p>Loading...</p>
            ) : (
                <ResponsiveContainer width="100%" height={400}>
                    <LineChart data={lapData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="lap" label={{ value: 'Lap Number', position: 'insideBottom', offset: -5 }} />
                        <YAxis label={{ value: 'Lap Time (s)', angle: -90, position: 'insideLeft' }} />
                        <Tooltip />
                        <Legend />
                        <Line type="monotone" dataKey="driver1Time" stroke="#FF6B35" name={driver1} />
                        <Line type="monotone" dataKey="driver2Time" stroke="#8B5CF6" name={driver2} />
                    </LineChart>
                </ResponsiveContainer>
            )}
        </div>
    );
}

export default DriverComparison;

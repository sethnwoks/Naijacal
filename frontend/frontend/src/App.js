import React, { useState } from 'react';
import './App.css';

const FREE_TRIAL_LIMIT = 5;

export default function App() {
    const [foodLog, setFoodLog] = useState('');
    const [message, setMessage] = useState('');
    const [calories, setCalories] = useState(null);
    const [parsedItems, setParsedItems] = useState([]);
    const [loading, setLoading] = useState(false);
    const [remainingTrials, setRemainingTrials] = useState(FREE_TRIAL_LIMIT);

    const handleParse = async () => {
        setMessage('');
        setCalories(null);
        setParsedItems([]);
        setLoading(true);

        if (foodLog.trim() === '') {
            setMessage('The food log is empty. Tell me what you ate!');
            setLoading(false);
            return;
        }

        if (foodLog.length > 500) {
            setMessage('Whoa! That is a bit too long. Try to keep it under 500 characters.');
            setLoading(false);
            return;
        }

        try {
            const response = await fetch(`${process.env.REACT_APP_API_URL}/parse-log`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ foodLog }),
            });
            const data = await response.json();

            if (!response.ok) {
                setMessage(data.error || 'Unable to process this request right now.');
                // Update trials even on error if the backend provided them (e.g., 429 errors)
                if (data.remaining_trials !== undefined) {
                    setRemainingTrials(data.remaining_trials);
                }
            } else {
                setParsedItems(data.parsed_items);
                setCalories(data.total_calories);
                setMessage('Successfully calculated!');
                
                // Update the dynamic trial counter
                if (data.remaining_trials !== undefined) {
                    setRemainingTrials(data.remaining_trials);
                }
            }
        } catch (err) {
            setMessage('Connection lost. Is the backend running?');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="main-bg">
            <header className="header">
                <span className="logo">NaijaCal</span>
                <span className="trial-badge">
                    {remainingTrials} {remainingTrials === 1 ? 'try' : 'tries'} left
                </span>
            </header>

            <main className="main-content">
                <div className="card main-card">
                    <div className="hero-copy">
                        <p className="eyebrow">AI-powered calorie estimate for Nigerian meals</p>
                        <h1 className="card-title">Log what you ate. See the calories in seconds.</h1>
                        <p className="hero-subtitle">
                            Anonymous trial mode is live. Account features are currently disabled while authentication is under review.
                        </p>
                    </div>
                    <textarea
                        value={foodLog}
                        onChange={(e) => setFoodLog(e.target.value)}
                        className="food-textarea"
                        placeholder="e.g. I had 2 plates of Jollof rice and 1 piece of chicken..."
                        disabled={loading}
                    />
                    <button onClick={handleParse} className="parse-btn" disabled={loading}>
                        {loading ? 'AI is thinking...' : 'Calculate Calories'}
                    </button>

                    {loading && (
                        <div style={{ textAlign: 'center', marginTop: 20 }}>
                            <div className="spinner"></div>
                        </div>
                    )}

                    {message && !loading && (
                        <div className="message" style={{ color: parsedItems.length > 0 ? '#2e7d32' : '#b42318' }}>
                            {message}
                        </div>
                    )}

                    {parsedItems.length > 0 && !loading && (
                        <div style={{ marginTop: 24, textAlign: 'left' }}>
                            <strong style={{ color: '#444', display: 'block', marginBottom: '12px' }}>Your Results:</strong>
                            <div className="results-list">
                                {parsedItems.map((item, idx) => (
                                    <div key={idx} className="result-item" style={{ background: '#fff9f0', padding: '12px', borderRadius: '10px', marginBottom: '10px', borderLeft: '4px solid #ffa726' }}>
                                        <div style={{ fontWeight: 'bold', color: '#333' }}>{item.item}</div>
                                        <div style={{ fontSize: '0.9rem', color: '#666' }}>
                                            {item.quantity} ➔ <span style={{ color: '#ffa726', fontWeight: 'bold' }}>
                                                {item.total_calories != null ? `${item.total_calories} cal` : 'Not found in database'}
                                            </span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                            <div style={{ marginTop: 20, textAlign: 'center', borderTop: '2px dashed #ffe0b2', paddingTop: '15px' }}>
                                <span style={{ fontSize: '1.4rem', fontWeight: '900', color: '#ff8f00' }}>{calories} Total Calories</span>
                            </div>
                        </div>
                    )}
                </div>
            </main>

            <footer className="footer" style={{ background: 'transparent', color: '#888', boxShadow: 'none' }}>
                © 2025 NaijaCal. Anonymous trial mode.
            </footer>
        </div>
    );
}

import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import '../index.css';
import logo2 from '../../src/topLogo.png';
import Footer from './Footer'; // Assuming Footer is a separate component

function NewSubmission() {
    const location = useLocation();
    const username = location.state?.username; // Keep the username passed from the previous page
    const [currentDateTime, setCurrentDateTime] = useState(new Date());
    const [selectedModelId, setSelectedModelId] = useState('');

    useEffect(() => {
        const timer = setInterval(() => {
            setCurrentDateTime(new Date());
        }, 1000);

        return () => {
            clearInterval(timer);
        };
    }, []);

    // Placeholder for the solver models data
    const solverModels = [
        { modelId: '123', title: 'Model One', notes: 'Some notes here.' },
        { modelId: '456', title: 'Model Two', notes: 'Additional notes here.' },
        // ...other models
    ];

    // Handler for when a model is selected from the dropdown
    const handleModelSelection = (event) => {
        setSelectedModelId(event.target.value);
    };

    return (
        <div className="landing">
            <img src={logo2} alt="solveMe Logo" className="top-logo"/>
            <h1>New Submission</h1>
            <div className="top-section">
                <div className="username-display">
                    <strong>Welcome, {username || 'Guest'}</strong>
                </div>
                <div className="date-time-box">
                    {currentDateTime.toLocaleDateString()} {currentDateTime.toLocaleTimeString()}
                </div>
            </div>
            <div className="solver-models-dropdown">
                <select value={selectedModelId} onChange={handleModelSelection} className="model-dropdown">
                    <option value="">Select a model</option>
                    {solverModels.map(model => (
                        <option key={model.modelId} value={model.modelId}>
                            {model.modelId} - {model.title} - {model.notes}
                        </option>
                    ))}
                </select>
            </div>
        </div>
    );
}

export default NewSubmission;

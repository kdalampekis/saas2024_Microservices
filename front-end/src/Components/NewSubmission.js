import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import '../index.css';
import logo2 from '../../src/topLogo.png';

function NewSubmission() {
    const location = useLocation();
    const username = location.state?.username;
    const [currentDateTime, setCurrentDateTime] = useState(new Date());
    const [selectedModel, setSelectedModel] = useState({ id: '', title: '' });

    useEffect(() => {
        const timer = setInterval(() => {
            setCurrentDateTime(new Date());
        }, 1000);

        return () => {
            clearInterval(timer);
        };
    }, []);

    const solverModels = [
        { modelId: '123', title: 'Model One', notes: 'Some notes here.' },
        { modelId: '456', title: 'Model Two', notes: 'Additional notes here.' },
    ];

    const metadata = [
        { id: '001', title: 'Metadata 1', uom: 'UOM 1' },
        { id: '002', title: 'Metadata 2', uom: 'UOM 2' },
        { id: '003', title: 'Metadata 3', uom: 'UOM 3' },
    ];

    const inputData = [
        { id: '101', title: 'Input Data 1', uom: 'UOM A' },
        { id: '102', title: 'Input Data 2', uom: 'UOM B' },
        { id: '103', title: 'Input Data 3', uom: 'UOM C' },
    ];

    const handleModelSelection = (event) => {
        const selectedId = event.target.value;
        const selected = solverModels.find(model => model.modelId === selectedId);
        setSelectedModel(selected || { id: '', title: '' });
    };

    return (
        <div className="landing">
            <img src={logo2} alt="solveMe Logo" className="top-logo" />
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
                <select value={selectedModel.id} onChange={handleModelSelection} className="model-dropdown">
                    <option value="">Select a model</option>
                    {solverModels.map(model => (
                        <option key={model.modelId} value={model.modelId}>
                            {model.modelId} - {model.title} - {model.notes}
                        </option>
                    ))}
                </select>
            </div>
            <div className="tables-container">
                <div className="table-container">
                    <h2>Metadata</h2>
                    <table>
                        <thead>
                        <tr>
                            <th style={{ width: '33%' }}>Metadata ID</th>
                            <th style={{ width: '33%' }}>Metadata Title</th>
                            <th style={{ width: '33%' }}>UOM</th>
                        </tr>
                        </thead>
                        <tbody>
                        {metadata.map((data, index) => (
                            <tr key={index}>
                                <td>{data.id}</td>
                                <td>{data.title}</td>
                                <td>{data.uom}</td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                </div>
                <div className="table-container">
                    <h2>Input Data</h2>
                    <table>
                        <thead>
                        <tr>
                            <th style={{ width: '33%' }}>Input Data ID</th>
                            <th style={{ width: '33%' }}>Input Data Title</th>
                            <th style={{ width: '33%' }}>UOM</th>
                        </tr>
                        </thead>
                        <tbody>
                        {inputData.map((data, index) => (
                            <tr key={index}>
                                <td>{data.id}</td>
                                <td>{data.title}</td>
                                <td>{data.uom}</td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                </div>
            </div>
            <div className="submission-section">
                <h3>New problem submission for {selectedModel.title || '<model>'}</h3>
                <button className="upload-button">
                    Upload submission metadata
                </button>
                <div className="form-buttons3">
                    <button className="create-button">Create</button>
                    <button className="cancel-button">Cancel</button>
                </div>
            </div>
        </div>
    );
}

export default NewSubmission;

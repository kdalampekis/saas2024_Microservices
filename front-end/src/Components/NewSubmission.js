import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import '../index.css';
import logo2 from '../../src/topLogo.png';

function NewSubmission() {
    const location = useLocation();
    const username = location.state?.username;

    const [selectedModel, setSelectedModel] = useState({ id: '', title: '' });
    const [currentMetadata, setCurrentMetadata] = useState([]);
    const [currentInputData, setCurrentInputData] = useState([]);
    const [metadataValues, setMetadataValues] = useState({});
    const [inputDataValues, setInputDataValues] = useState({});
    const [submissionData, setSubmissionData] = useState(null);

    function Clock() {
        const [currentDateTime, setCurrentDateTime] = useState(new Date());

        useEffect(() => {
            const timer = setInterval(() => {
                setCurrentDateTime(new Date());
            }, 1000);
            return () => clearInterval(timer);
        }, []);

        return (
            <div className="date-time-box">
                {currentDateTime.toLocaleDateString()} {currentDateTime.toLocaleTimeString()}
            </div>
        );
    }


    const handleMetadataChange = (id, value) => {
        setMetadataValues(prev => ({
            ...prev,
            [id]: value
        }));
    };

    const handleInputDataChange = (id, value) => {
        setInputDataValues(prev => ({
            ...prev,
            [id]: value
        }));
    };

    const solverModels = [
        { modelId: '1', title: 'queens', notes: 'Solve the n-queens puzzle.' },
        { modelId: '2', title: 'solve-vrp', notes: 'Optimize vehicle routing paths.' },
        { modelId: '3', title: 'bin_packing', notes: 'Optimize bin packing using weights.' },
        { modelId: '4', title: 'linear_programming', notes: 'Solve linear programming problems.' },
        { modelId: '5', title: 'job_shop', notes: 'Optimize job shop scheduling.' },
        { modelId: '6', title: 'multiple_knapsack', notes: 'Solve multiple knapsack problems.' },
        { modelId: '7', title: 'max_flow', notes: 'Calculate maximum flow in networks.' },
        { modelId: '8', title: 'lin_sum_assignment', notes: 'Optimize linear sum assignment.' },
    ];

    const modelSpecificData = {
        '1': { // Model ID for 'queens'
            metadata: [
                { id: '001', title: 'Chessboard Size', uom: 'Squares', type: 'number' }
            ],
            inputData: [
                { id: '101', title: 'Starting Position', uom: 'Coordinates', type: 'text' } // Assuming text format for simplicity
            ]
        },
        '2': { // Model ID for 'solve-vrp'
            metadata: [
                { id: '002', title: 'Vehicle Counts', uom: 'Vehicles', type: 'number' }
            ],
            inputData: [
                { id: '102', title: 'Locations File', uom: 'File', type: 'file' },
                { id: '103', title: 'Number of Vehicles', uom: 'Vehicles', type: 'number' },
                { id: '104', title: 'Vehicles Capacity', uom: 'Capacity', type: 'number' }
            ]
        },
        '3': { // Model ID for 'bin_packing'
            metadata: [],
            inputData: [
                { id: '105', title: 'Weights', uom: 'Weights list', type: 'text' }, // Comma-separated weights
                { id: '106', title: 'Bin Capacity', uom: 'Max number', type: 'number' }
            ]
        },
        '4': { // Model ID for 'linear_programming'
            metadata: [],
            inputData: [
                { id: '107', title: 'Objective Coefficient', uom: 'Tuple', type: 'text' },
                { id: '108', title: 'Constraints Coefficient', uom: 'Matrix', type: 'text' },
                { id: '109', title: 'Bounds', uom: 'Tuple', type: 'text' }
            ]
        },
        '5': { // Model ID for 'job_shop'
            metadata: [],
            inputData: [
                { id: '110', title: 'Jobs Data', uom: 'Matrix of Tuples', type: 'text' } // Nested tuples represented in textarea
            ]
        },
        '6': { // Model ID for 'multiple_knapsack'
            metadata: [],
            inputData: [
                { id: '111', title: 'Weights', uom: 'Matrix', type: 'text' }, // Matrix of weights
                { id: '112', title: 'Values', uom: 'Matrix', type: 'text' }, // Matrix of values
                { id: '113', title: 'Bin Capacity', uom: 'Capacity', type: 'number' },
                { id: '114', title: 'Number of Bins', uom: 'Number', type: 'number' }
            ]
        },
        '7': { // Model ID for 'max_flow'
            metadata: [],
            inputData: [
                { id: '115', title: 'Start Nodes', uom: 'List', type: 'text' }, // Comma-separated list of start nodes
                { id: '116', title: 'End Nodes', uom: 'List', type: 'text' }, // Comma-separated list of end nodes
                { id: '117', title: 'Capacities', uom: 'List', type: 'text' }, // Comma-separated list of capacities
                { id: '118', title: 'Source', uom: 'Node', type: 'number'},
                { id: '119', title: 'Sink', uom: 'Node', type: 'number' }
            ]
        },
        '8': { // Model ID for 'lin_sum_assignment'
            metadata: [],
            inputData: [
                { id: '120', title: 'Costs', uom: 'Matrix', type: 'textarea' } // Costs matrix
            ]
        }
    };

    const handleModelSelection = (event) => {
        const selectedId = event.target.value;
        const selected = solverModels.find(model => model.modelId === selectedId);
        setSelectedModel(selected || { id: '', title: '' });
        const modelData = selected ? (modelSpecificData[selectedId] || { metadata: [], inputData: [] }) : { metadata: [], inputData: [] };
        setCurrentMetadata(modelData.metadata);
        setCurrentInputData(modelData.inputData);
        setMetadataValues({});
        setInputDataValues({});
        setSubmissionData(null); // Clear previous submission data on model change
    };

    const handleSubmit = () => {
        const problemData = {
            typeOfProblem: selectedModel.title,
            inputData: {...inputDataValues}
        };
        setSubmissionData(problemData);
    };

    function InputComponent({ dataId, dataType, value, handleChange }) {
        const inputKey = React.useMemo(() => `${dataId}-${dataType}`, [dataId, dataType]);  // Ensures stable key
        return (
            <input
                key={inputKey}
                type={dataType}
                value={value}
                //onChange={(e) => handleChange(dataId, dataType === 'file' ? e.target.files[0] : e.target.value)}
                className={dataType === 'file' ? 'file-input' : 'text-input'}
            />
        );
    }
    currentInputData.map((data) => (
        <tr key={data.id}>
            <td>{data.id}</td>
            <td>{data.title}</td>
            <td>{data.uom}</td>
            <td>
                <InputComponent
                    dataId={data.id}
                    dataType={data.type || 'text'}
                    value={inputDataValues[data.id] || ''}
                    handleChange={handleInputDataChange}
                />
            </td>
        </tr>
    ))

    return (
        <div className="landing">
            <img src={logo2} alt="solveMe Logo" className="top-logo"/>
            <h1>New Submission</h1>
            <div className="top-section">
                <div className="username-display">
                    <strong>Welcome, {username || 'Guest'}</strong>
                </div>
                <Clock/>
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
                            <th>Metadata ID</th>
                            <th>Metadata Title</th>
                            <th>UOM</th>
                            <th>Value</th>
                        </tr>
                        </thead>
                        <tbody>
                        {currentMetadata.map(data => (
                            <tr key={data.id}>
                                <td>{data.id}</td>
                                <td>{data.title}</td>
                                <td>{data.uom}</td>
                                <td>
                                    <InputComponent
                                        dataId={data.id}
                                        dataType={data.type || 'text'}
                                        value={metadataValues[data.id]}
                                        handleChange={handleMetadataChange}
                                    />
                                </td>
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
                            <th>Input Data ID</th>
                            <th>Input Data Title</th>
                            <th>UOM</th>
                            <th>Value</th>
                        </tr>
                        </thead>
                        <tbody>
                        {currentInputData.map(data => (
                            <tr key={data.id}>
                                <td>{data.id}</td>
                                <td>{data.title}</td>
                                <td>{data.uom}</td>
                                <td>
                                    <InputComponent
                                        dataId={data.id}
                                        dataType={data.type || 'text'}
                                        value={inputDataValues[data.id]}
                                        handleChange={handleInputDataChange}
                                    />
                                </td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                </div>
            </div>

            <div className="submission-section">
                <h3>New problem submission for {selectedModel.title || '<model not selected>'}</h3>
                <button className="upload-button" onClick={handleSubmit}>Create Submission Data</button>
                <div className="form-buttons">
                    <button className="cancel-button" onClick={() => setSubmissionData(null)}>Clear</button>
                </div>
                {submissionData && (
                    <div className="submission-data">
                        <h4>Submission Data:</h4>
                        <pre>{JSON.stringify(submissionData, null, 2)}</pre>
                    </div>
                )}
            </div>
        </div>

/*        <div className="submission-section">
            <h3>New problem submission for {selectedModel.title || '<model not selected>'}</h3>
            <button className="upload-button">Upload submission metadata</button>
             <div className="form-buttons">
            <Link to="/EditSubmission" className="create-button">Create</Link>
            <button className="cancel-button">Cancel</button>
            </div>
            </div>
    <   /div>*/
);
}

export default NewSubmission;

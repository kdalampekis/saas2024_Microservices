import React, { useState, useEffect, useRef } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import '../index.css';
import logo2 from '../../src/topLogo.png';

function NewSubmission() {
    const location = useLocation();
    const navigate = useNavigate();
    const username = location.state?.username || 'Guest';

    const [selectedModel, setSelectedModel] = useState({ id: '', title: '' });
    const [currentInputData, setCurrentInputData] = useState([]);
    const [errorMessage, setErrorMessage] = useState('');
    const [allFieldsFilled, setAllFieldsFilled] = useState(true);
    const [creditBalance, setCreditBalance] = useState(0);
    const [isCreateDisabled, setIsCreateDisabled] = useState(false);

    const metadataRefs = useRef({});
    const inputDataRefs = useRef({});

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

    const solverModels = [
        { modelId: '1', title: 'vrp', notes: 'Optimize vehicle routing paths.', cost: 100 },
        { modelId: '2', title: 'queens', notes: 'Solve the n-queens puzzle.', cost: 100 },
        { modelId: '3', title: 'bin_packing', notes: 'Optimize bin packing using weights.', cost: 100 },
        { modelId: '4', title: 'linear_programming', notes: 'Solve linear programming problems.', cost: 100 },
        { modelId: '5', title: 'job_shop', notes: 'Optimize job shop scheduling.', cost: 100 },
        { modelId: '6', title: 'multiple_knapsack', notes: 'Solve multiple knapsack problems.', cost: 100 },
        { modelId: '7', title: 'max_flow', notes: 'Calculate maximum flow in networks.', cost: 100 },
        { modelId: '8', title: 'lin_sum_assignment', notes: 'Optimize linear sum assignment.', cost: 100 },
    ];

    const staticMetadata = [
        { id: 'username', title: 'Username', uom: 'text', type: 'text', value: username },
        { id: 'credit_cost', title: 'Credit Cost', uom: 'credits', type: 'number', value: '100' }
    ];

    const modelSpecificData = {
        '1': { inputData: [{ id: 'locations_file', title: 'Locations File', uom: 'File', type: 'file' }, { id: 'number_of_locations', title: 'Number of Vehicles', uom: 'Vehicles', type: 'text' }, { id: 'number_of_vehicles', title: 'Number of Locations', uom: 'Locations', type: 'text' }, { id: 'vehicle_capacity', title: 'Vehicles Capacity', uom: 'Capacity', type: 'text' }] },
        '2': { inputData: [{ id: 'board_size', title: 'Chessboard Size', uom: 'Squares', type: 'text' }] },
        '3': { inputData: [{ id: 'weights', title: 'Weights', uom: 'Weights list', type: 'text' }, { id: 'bin_capacity', title: 'Bin Capacity', uom: 'Max number', type: 'text' }] },
        '4': { inputData: [{ id: 'objective_coeffs', title: 'Objective Coefficient', uom: 'Tuple', type: 'text' }, { id: 'constraints_coeffs', title: 'Constraints Coefficient', uom: 'Matrix', type: 'text' }, { id: 'bounds', title: 'Bounds', uom: 'Tuple', type: 'text' }] },
        '5': { inputData: [{ id: 'jobs_data', title: 'Jobs Data', uom: 'Matrix of Tuples', type: 'text' }] },
        '6': { inputData: [{ id: 'weights', title: 'Weights', uom: 'Matrix', type: 'text' }, { id: 'values', title: 'Values', uom: 'Matrix', type: 'text' }, { id: 'bin_capacity', title: 'Bin Capacity', uom: 'Capacity', type: 'text' }, { id: 'num_bins', title: 'Number of Bins', uom: 'Number', type: 'text' }] },
        '7': { inputData: [{ id: 'start_nodes', title: 'Start Nodes', uom: 'List', type: 'text' }, { id: 'end_nodes', title: 'End Nodes', uom: 'List', type: 'text' }, { id: 'capacities', title: 'Capacities', uom: 'List', type: 'text' }, { id: 'source', title: 'Source', uom: 'Node', type: 'text' }, { id: 'sink', title: 'Sink', uom: 'Node', type: 'text' }] },
        '8': { inputData: [{ id: 'costs', title: 'Costs', uom: 'Matrix', type: 'textarea' }] }
    };

    const MetadataApiEndpoints = {
        '1': 'http://localhost:8003/problem/create-metadata/vrp/',
        '2': 'http://localhost:8003/problem/create-metadata/queens/',
        '3': 'http://localhost:8003/problem/create-metadata/bin_packing/',
        '4': 'http://localhost:8003/problem/create-metadata/linear_programming/',
        '5': 'http://localhost:8003/problem/create-metadata/job_shop/',
        '6': 'http://localhost:8003/problem/create-metadata/multiple_knapsack/',
        '7': 'http://localhost:8003/problem/create-metadata/max_flow/',
        '8': 'http://localhost:8003/problem/create-metadata/lin_sum_assignment/',
    };

    useEffect(() => {
        initializeAndFetchCreditBalance(username);
    }, [username]);

    const initializeAndFetchCreditBalance = async (id) => {
        try {
            const initializeResponse = await fetch(`http://localhost:8002/credits/initialize_user_credits/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ user_id: id }),
            });

            if (!initializeResponse.ok && initializeResponse.status !== 400) {
                throw new Error(`Failed to initialize credit balance: ${initializeResponse.statusText}`);
            }

            const fetchResponse = await fetch(`http://localhost:8002/credits/balance/${id}/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (!fetchResponse.ok) {
                throw new Error(`Failed to fetch credit balance: ${fetchResponse.statusText}`);
            }

            const fetchData = await fetchResponse.json();
            setCreditBalance(fetchData.balance);
        } catch (error) {
            setErrorMessage(error.message);
        }
    };

    const handleModelSelection = (event) => {
        const selectedId = event.target.value;
        const selectedModel = solverModels.find(model => model.modelId === selectedId);
        setSelectedModel(selectedModel || { id: '', title: '' });
        if (selectedModel) {
            const modelData = modelSpecificData[selectedId] || { inputData: [] };
            setCurrentInputData(modelData.inputData);
            metadataRefs.current = {};
            inputDataRefs.current = {};

            // Check if the user has enough credits for the selected model
            if (creditBalance < selectedModel.cost) {
                setIsCreateDisabled(true);
                setErrorMessage('Not enough credits!');  // Update this line
            } else {
                setIsCreateDisabled(false);
                setErrorMessage('');
            }
        } else {
            setCurrentInputData([]);
        }
        setAllFieldsFilled(true); // Reset allFieldsFilled to true
    };

    const handleClear = () => {
        setAllFieldsFilled(true); // Reset allFieldsFilled to true
        setErrorMessage(''); // Clear any existing error messages
    };



    const handleApiCall = async () => {
        const formData = new FormData();
        let allFieldsFilled = true;

        // Collect static metadata values and check if any are empty
        staticMetadata.forEach(data => {
            const value = metadataRefs.current[data.id]?.value || data.value;
            formData.append(data.id, value);
        });

        // Collect input data values and check if any are empty
        currentInputData.forEach(data => {
            const inputElement = inputDataRefs.current[data.id];
            const value = data.type === 'file' ? inputElement?.files[0] : inputElement?.value;
            formData.append(data.id, value);
            if (value === '' || value === undefined) {
                allFieldsFilled = false;
            }
        });

        setAllFieldsFilled(allFieldsFilled);

        if (!allFieldsFilled) {
            setErrorMessage('All the inputs must be filled');
            return;
        }

        const apiUrl = MetadataApiEndpoints[selectedModel.modelId];

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const result = await response.json();
                console.log('API call successful:', result);

                // Call SpendCreditsView to deduct credits
                const spendCreditsResponse = await fetch(`http://localhost:8002/credits/${username}/spend/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ credits: selectedModel.cost }),
                });

                if (spendCreditsResponse.ok) {
                    const spendCreditsResult = await spendCreditsResponse.json();
                    console.log('Credits deducted successfully:', spendCreditsResult);
                    navigate('/MySubmissions', { state: { username: username } });
                } else {
                    const errorData = await spendCreditsResponse.json();
                    setErrorMessage(`Failed to deduct credits: ${errorData.error}`);
                }
            } else {
                const errorData = await response.json();
                setErrorMessage(`API call failed: ${errorData.message}`);
            }
        } catch (error) {
            setErrorMessage(`API call failed: ${error.message}`);
            console.log(formData);
        }
    };

        function InputComponent({ dataId, dataType, inputRef, defaultValue }) {
            return (
                <input
                    type={dataType}
                    ref={inputRef}
                    defaultValue={defaultValue}
                    className={dataType === 'file' ? 'file-input' : 'text-input'}
                />
            );
        }

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
                            {model.modelId} - {model.title} - {model.notes} ({model.cost} credits)
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
                        {staticMetadata.map(data => (
                            <tr key={data.id}>
                                <td>{data.id}</td>
                                <td>{data.title}</td>
                                <td>{data.uom}</td>
                                <td>{data.value}</td>
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
                                        dataType={data.type}
                                        inputRef={el => inputDataRefs.current[data.id] = el}
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
                <div className="form-buttons">
                    <button className="cancel-button" onClick={handleClear}>Clear</button>
                    <button className="create-button" style={{ backgroundColor: 'green', color: 'white' }} onClick={handleApiCall} disabled={isCreateDisabled}>Create</button>
                </div>
                {errorMessage && (
                    <div className="error-message">
                        <p>{errorMessage}</p>
                    </div>
                )}
            </div>
        </div>
    );
}

export default NewSubmission;
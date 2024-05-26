import React, { useState, useEffect } from 'react';
import '../index.css';
import logo2 from '../../src/topLogo.png';
import { useLocation, useNavigate } from 'react-router-dom';

function MySubmissions() {
    const location = useLocation();
    const navigate = useNavigate();
    const username = location.state?.username || 24; // For testing, default to 24 if username is not provided
    const [currentDateTime, setCurrentDateTime] = useState(new Date());
    const [creditBalance, setCreditBalance] = useState(0);
    const [error, setError] = useState(null);

    useEffect(() => {
        const timer = setInterval(() => {
            setCurrentDateTime(new Date());
        }, 1000);

        return () => {
            clearInterval(timer);
        };
    }, []);

    useEffect(() => {
        const initializeAndFetchCreditBalance = async () => {
            try {
                // Fetch user's credit balance to check if it exists
                let fetchResponse = await fetch(`http://localhost:8002/credits/balance/${username}/`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });

                if (fetchResponse.status === 404) {
                    // If balance does not exist, initialize it
                    const initializeResponse = await fetch(`http://localhost:8002/credits/initialize_user_credits/`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ user_id: username }),
                    });

                    if (!initializeResponse.ok) {
                        throw new Error(`Failed to initialize credit balance: ${initializeResponse.statusText}`);
                    }

                    console.log('Initialization Success');

                    // Fetch user's credit balance again after initialization
                    fetchResponse = await fetch(`http://localhost:8002/credits/balance/${username}/`, {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                    });

                    if (!fetchResponse.ok) {
                        throw new Error(`Failed to fetch credit balance: ${fetchResponse.statusText}`);
                    }
                }

                const fetchData = await fetchResponse.json();
                console.log('Fetch Success:', fetchData);
                setCreditBalance(fetchData.balance);
            } catch (error) {
                console.error('Error:', error);
                setError(error.message);
            }
        };

        initializeAndFetchCreditBalance();
    }, [username]);

    // Example data for the table
    const submissions = [
        { name: 'Submission 1', createdOn: 'Date 1', status: 'ready' },
        { name: 'Submission 2', createdOn: 'Date 2', status: 'not ready' },
        // ... other submissions
    ];

    // Add any functionality for when the "New Problem" button is clicked
    const handleNewClick = () => {
        navigate('/NewSubmission', { state: { username: username } }); // Navigate and pass username
    };

    return (
        <div className="landing">
            <img src={logo2} alt="solveMe Logo" className="top-logo"/>
            <h1>My Submissions</h1>
            <div className="top-section">
                <div className="username-display">
                    <strong>Welcome, {username || 'Guest'}</strong>
                </div>
                <div className="date-time-box">
                    {currentDateTime.toLocaleDateString()} {currentDateTime.toLocaleTimeString()}
                </div>
            </div>
            <div className="credit-balance-box">
                <h2>Credit Balance</h2>
                {error ? (
                    <p>{error}</p>
                ) : (
                    <p>{creditBalance}</p>
                )}
            </div>
            <div className="submissions-table">
                <table>
                    <thead>
                    <tr>
                        <th>Name</th>
                        <th>Created On</th>
                        <th>Status</th>
                        <th colSpan="4">Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    {submissions.map((submission, index) => (
                        <tr key={index}>
                            <td>{submission.name}</td>
                            <td>{submission.createdOn}</td>
                            <td>{submission.status}</td>
                            <td>
                                <button>View/Edit</button>
                            </td>
                            <td>
                                <button>Run</button>
                            </td>
                            <td>
                                <button>View Results</button>
                            </td>
                            <td>
                                <button className="delete-button">Delete</button>
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
            <button className="new-problem-button" onClick={handleNewClick}>
                New Problem
            </button>
        </div>
    );
}

export default MySubmissions;
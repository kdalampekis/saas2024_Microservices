import React, { useState, useEffect } from 'react';
import '../index.css';
import logo2 from '../../src/topLogo.png';
import { useLocation, useNavigate } from 'react-router-dom';

function MySubmissions() {
    const location = useLocation();
    const navigate = useNavigate();
    const username = location.state?.username || '24'; // For testing, default to 24 if username is not provided
    const [currentDateTime, setCurrentDateTime] = useState(new Date());
    const [creditBalance, setCreditBalance] = useState(0);
    const [creditsToAdd, setCreditsToAdd] = useState(0); // State for the input value
    const [userId, setUserId] = useState(username); // State for the user ID input
    const [error, setError] = useState(null);

    useEffect(() => {
        const timer = setInterval(() => {
            setCurrentDateTime(new Date());
        }, 1000);

        return () => {
            clearInterval(timer);
        };
    }, []);

    const initializeAndFetchCreditBalance = async (id) => {
        try {
            // Initialize user's credit balance
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

            console.log('Initialization Success');

            // Fetch user's credit balance after initialization
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
            console.log('Fetch Success:', fetchData);
            setCreditBalance(fetchData.balance);
        } catch (error) {
            console.error('Error initializing and fetching credit balance:', error);
            setError(error.message);
        }
    };

    useEffect(() => {
        initializeAndFetchCreditBalance(username);
    }, [username]);

    const handleNewClick = () => {
        navigate('/NewSubmission', { state: { username: username } }); // Navigate and pass username
    };

    const handleBuyCredits = async () => {
        try {
            if (!userId) {
                throw new Error('User ID is required');
            }

            const response = await fetch(`http://localhost:8002/credits/purchase/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ user_id: userId, credits: creditsToAdd }),
            });

            if (!response.ok) {
                throw new Error(`Failed to buy credits: ${response.statusText}`);
            }

            const data = await response.json();
            console.log('Buy Credits Success:', data);

            // Reload the page
            window.location.reload();
        } catch (error) {
            console.error('Error buying credits:', error);
            setError(error.message);
        }
    };

    // Example data for the table
    const submissions = [
        { name: 'Submission 1', createdOn: 'Date 1', status: 'ready' },
        { name: 'Submission 2', createdOn: 'Date 2', status: 'not ready' },
        // ... other submissions
    ];

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
                <div className="buy-credits">
                    <input
                        type="text"
                        value={userId}
                        onChange={(e) => setUserId(e.target.value)}
                        placeholder="Enter your user ID"
                    />
                    <input
                        type="number"
                        value={creditsToAdd}
                        onChange={(e) => setCreditsToAdd(Number(e.target.value))}
                        placeholder="Enter credits to buy"
                    />
                    <button onClick={handleBuyCredits}>Buy Credits</button>
                </div>
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
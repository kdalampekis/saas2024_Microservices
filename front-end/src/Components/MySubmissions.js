import React, { useState, useEffect } from 'react';
import '../index.css';
import logo2 from '../../src/topLogo.png';
import { useLocation, useNavigate } from 'react-router-dom';

function MySubmissions() {
    const location = useLocation();
    const navigate = useNavigate();
    const username = location.state?.username || 'Guest';
    const [currentDateTime, setCurrentDateTime] = useState(new Date());
    const [creditBalance, setCreditBalance] = useState(0);
    const [creditsToAdd, setCreditsToAdd] = useState(0);
    const [userId, setUserId] = useState(null); // Initialize userId as null
    const [error, setError] = useState(null);
    const [submissions, setSubmissions] = useState([]);

    useEffect(() => {
        const timer = setInterval(() => {
            setCurrentDateTime(new Date());
        }, 1000);

        return () => {
            clearInterval(timer);
        };
    }, []);

    const fetchUserId = async (username) => {
        console.log(`fetchUserId called for username: ${username}`);  // Log to ensure the function is called

        try {
            const response = await fetch(`http://localhost:8002/users/get_id_by_username/${username}/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.status === 404) {
                console.log(`User ${username} not found. Creating new user.`);
                await createUser(username);  // Call the function to create a new user
                return;
            }

            if (!response.ok) {
                throw new Error(`Failed to fetch user ID: ${response.statusText}`);
            }

            const data = await response.json();
            setUserId(data.user_id);  // Assuming user_id is returned in the response

            console.log(`%cUSER'S ID IS: ${data.user_id}`, 'color: green; font-weight: bold;');
        } catch (error) {
            setError(`Error fetching user ID: ${error.message}`);
            console.error(`Error fetching user ID: ${error.message}`);
        }
    };

// Helper function to create a new user and re-fetch their user ID
    const createUser = async (username) => {
        try {
            const response = await fetch(`http://localhost:8002/credits/initialize_user_credits/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,  // Use the correct username key
                }),
            });

            if (!response.ok) {
                throw new Error(`Failed to create new user: ${response.statusText}`);
            }

            const data = await response.json();
            setUserId(data.user_id);  // Assuming the new user ID is returned in the response

            console.log(`%cNew USER CREATED: ID = ${data.user_id}, Username = ${username}`, 'color: blue; font-weight: bold;');
        } catch (error) {
            setError(`Error creating new user: ${error.message}`);
            console.error(`Error creating new user: ${error.message}`);
        }
    };




    const fetchCreditBalance = async (username) => {
        try {
            const response = await fetch(`http://localhost:8002/credits/balance/${username}/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error(`Failed to fetch credit balance: ${response.statusText}`);
            }

            const data = await response.json();
            setCreditBalance(data.balance);
        } catch (error) {
            setError(`Error fetching credit balance: ${error.message}`);
        }
    };

    const fetchUserSubmissions = async (username) => {
        if (!username) {
            console.error('Username is not defined');
            return;
        }
        try {
            const response = await fetch(`http://localhost:8003/problem/submissions/${username}/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error(`Failed to fetch submissions: ${response.statusText}`);
            }

            const data = await response.json();
            setSubmissions(data);
        } catch (error) {
            setError(`Error fetching submissions: ${error.message}`);
        }
    };

    useEffect(() => {
        if (username) {
            console.log(`Fetching data for user: ${username}`);  // Add this to check if the effect runs
            fetchUserId(username);  // Fetch or create user ID
            fetchCreditBalance(username);  // Fetch user's credit balance
            fetchUserSubmissions(username);  // Fetch user's submissions
        } else {
            console.error('Username is not defined');
        }
    }, [username]);



    const handleNewClick = () => {
        navigate('/NewSubmission', { state: { username: username } });
    };

    const deleteSubmission = async (submissionId) => {
        try {
            const response = await fetch(`http://localhost:8001/metadata/delete/${submissionId}/`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                throw new Error(`Failed to delete submission: ${response.statusText}`);
            }

            // Remove the deleted submission from the state
            const updatedSubmissions = submissions.filter(submission => submission.submission_id !== submissionId);
            setSubmissions(updatedSubmissions);
        } catch (error) {
            setError(`Error deleting submission: ${error.message}`);
        }
    };

    const runSubmission = async (submissionId) => {
        try {
            const response = await fetch(`http://localhost:8003/problem/submit_problem/${submissionId}/`, {
                method: 'POST'
            });

            if (!response.ok) {
                throw new Error(`Failed to execute submission: ${response.statusText}`);
            }
        } catch (error) {
            setError(`Error submitting submission: ${error.message}`);
        }
    };
    
    const viewResults = async (submissionId) => {

        navigate('/ViewSubmissionResults', { state: { username, submissionId } });

        // try {
        //     console.log(`DEBUG: Fetching results for submission ID: ${submissionId}`);
            
        //     const response = await fetch(`http://localhost:8005/get-results/${submissionId}/`, {
        //         method: 'GET'
        //     });
    
        //     // Debugging: Check if the response is ok
        //     console.log(`DEBUG: Response status: ${response.status}`);
            
        //     if (!response.ok) {
        //         throw new Error(`Failed to fetch results: ${response.statusText}`);
        //     }
    
        //     // Parse the response JSON
        //     const data = await response.json();
        //     console.log("DEBUG: Data received from the API:", data);
    
        //     // Show the data in an alert pop-up window
        //     alert(`Results: ${JSON.stringify(data)}`);
    
        //     // Optionally, return the data
        //     return data;
            
        // } catch (error) {
        //     // Debugging: Print error details
        //     console.log(`DEBUG: Error occurred: ${error.message}`);
        //     setError(`Error fetching results: ${error.message}`);
        // }
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

            window.location.reload();
        } catch (error) {
            setError(error.message);
        }
    };

    const getStatusText = (submission) => {
        if (submission.status === 'Executed') {
            return 'Executed';
        } else if (submission.status === 'Ready') {
            return 'Ready';
        } else {
            return 'Not Ready';
        }
    };

    // Updated Logout Function with checks
    const handleLogout = async () => {
        navigate('/login');
        const token = localStorage.getItem('token');
        if (!token) {
            setError('No token found, cannot log out.');
            return;
        }

        try {
            const response = await fetch(`http://localhost:8000/logout/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Token ${token}`,  // Token format
                    'Content-Type': 'application/json',
                },
            });

            if (response.status === 401) {
                setError('Session has expired. Please log in again.');
                localStorage.removeItem('token');
                navigate('/login');
            } else if (!response.ok) {
                throw new Error('Failed to logout');
            } else {
                // Successful logout
                localStorage.removeItem('token');
                navigate('/login');
            }
        } catch (error) {
            setError(`Error logging out: ${error.message}`);
        }
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
                {/* Add a Logout button */}
                <div className="logout-button">
                    <button onClick={handleLogout}>Logout</button>
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
                            <td>{submission.submission_id}</td>
                            <td>{new Date(submission.date).toLocaleString()}</td>
                            <td>{getStatusText(submission)}</td>
                            <td>
                                <button>View/Edit</button>
                            </td>
                            <td>
                                <button
                                    onClick={() => {
                                        if (window.confirm("Are you sure you want to run this submission? **Updated**")) {
                                            runSubmission(submission.submission_id);
                                        }
                                    }}
                                >
                                Run
                                </button>
                            </td>
                            <td>
                                <button
                                onClick={() => {
                                    if (window.confirm("Are you sure you want to see the results?")) {
                                        viewResults(submission.submission_id);
                                    }
                                }}
                                >
                                View Results
                                </button>
                            </td>
                            <td>
                                <button className="delete-button"
                                        onClick={() => {
                                            if (window.confirm("Are you sure you want to delete this submission?")) {
                                                deleteSubmission(submission.submission_id);
                                            }
                                        }}>
                                    Delete
                                </button>
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

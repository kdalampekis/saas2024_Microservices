import React, { useState, useEffect } from 'react';
import '../index.css';
import logo2 from '../../src/topLogo.png';
import { useLocation, useNavigate } from 'react-router-dom';

function MySubmissions() {
    const location = useLocation();
    const navigate = useNavigate();
    const username = location.state?.username;
    const [currentDateTime, setCurrentDateTime] = useState(new Date());

    useEffect(() => {
        const timer = setInterval(() => {
            setCurrentDateTime(new Date());
        }, 1000);

        return () => {
            clearInterval(timer);
        };
    }, []);

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
            <div className="submissions-table">
                <table>
                    <thead>
                    <tr>
                        <th>Name</th>
                        <th>Created On</th>
                        <th>Status</th>
                        <th colSpan="3">Actions</th>
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

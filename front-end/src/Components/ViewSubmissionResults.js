import React, { useState, useEffect } from 'react';
import '../index.css';
import logo2 from '../../src/topLogo.png';
import { useLocation, useNavigate } from 'react-router-dom';

function ViewSubmissionResults() {
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
        { name:"I AM", description: "he wanted to be HIM", value: "1000$" },
        { name:"I AM NOT", description: "he did not want to be HIM", value: "2500$" },
        // ... other submissions
    ];

    // Add any functionality for when the "New Problem" button is clicked
    const handleNewClick = () => {
        navigate('/NewSubmission', { state: { username: username } }); // Navigate and pass username
    };

    return (
        <div className="landing">
            <img src={logo2} alt="solveMe Logo" className="top-logo"/>
            <h1>View Submission Results</h1>
            <div className="top-section">
                <div className="username-display">
                    <strong>status(username,company,account status, logout)</strong>
                </div>
                <div className="date-time-box">
                    {currentDateTime.toLocaleDateString()} {currentDateTime.toLocaleTimeString()}
                </div>
            </div>

            <div className="metadata-table">
                <table>
                    <thead>
                    <tr>
                        <th>Name</th>
                        <th>Description</th>
                        <th>Value</th>
                    </tr>
                    </thead>
                    <tbody>
                    {submissions.map((submission, index) => (
                        <tr key={index}>
                            <td>{submission.name}</td>
                            <td>{submission.description}</td>
                            <td>{submission.value}</td>
                        </tr>
                    ))}
                    </tbody>
                </table>

            </div>
        </div>
    );
}

export default ViewSubmissionResults;
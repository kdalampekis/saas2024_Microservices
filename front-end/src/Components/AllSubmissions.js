import React, { useState, useEffect } from 'react';
import '../index.css';
import logo2 from '../../src/topLogo.png';
import { Link, useLocation, useNavigate } from 'react-router-dom';

function AllSubmissions() {
    const location = useLocation();
    const navigate = useNavigate();
    const username = location.state?.username;
    const [currentDateTime, setCurrentDateTime] = useState(new Date());
    const [submissions, setSubmissions] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        const timer = setInterval(() => {
            setCurrentDateTime(new Date());
        }, 1000);

        return () => {
            clearInterval(timer);
        };
    }, []);

    const fetchAllSubmissions = async () => {
        try {
            const response = await fetch(`http://localhost:8003/problem/submissions/`, {
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
        fetchAllSubmissions();
    }, []);


    const getStatusText = (submission) => {
        if (submission.status === 'Executed') {
            return 'Executed';
        } else if (submission.status === 'Ready') {
            return 'Ready';
        } else {
            return 'Not Ready';
        }
    };

    return (
        <div className="landing">
            <img src={logo2} alt="solveMe Logo" className="top-logo"/>
            <h1>All Submissions</h1>
            <div className="top-section">
                <div className="username-display">
                    <strong>Activity</strong>
                </div>
                <div className="date-time-box">
                    {currentDateTime.toLocaleDateString()} {currentDateTime.toLocaleTimeString()}
                </div>
            </div>
            <div className="submissions-table">
                {error && <p>{error}</p>}
                <table>
                    <thead>
                    <tr>
                        <th>Creator</th>
                        <th>Submission ID</th>
                        <th>Created On</th>
                        <th>Status</th>
                        <th colSpan="4">Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    {submissions.map((submission, index) => (
                        <tr key={index}>
                            <td>{submission.username}</td>
                            <td>{submission.submission_id}</td> {/* Display submission ID here */}
                            <td>{new Date(submission.date).toLocaleString()}</td>
                            <td>{getStatusText(submission)}</td>
                            <td>
                                <button>View/Edit</button>
                            </td>
                            <td>
                                <button>Run</button>
                            </td>
                            <td>
                                <Link to="/ViewSubmissionResults" className="btn btn-secondary">View Results</Link>
                            </td>
                            <td>
                                <button className="delete-button">Delete</button>
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

export default AllSubmissions;
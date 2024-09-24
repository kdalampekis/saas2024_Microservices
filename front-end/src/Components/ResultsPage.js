import React, { useState, useEffect } from 'react';
import '../index.css';
import logo2 from '../../src/topLogo.png';
import { useLocation } from 'react-router-dom';
import Chart from 'chart.js/auto';  // Import Chart.js for results visualization

function ResultsPage() {
    const location = useLocation();
    const username = location.state?.username || 'Guest';
    const submissionId = location.state?.submissionId;
    const [currentDateTime, setCurrentDateTime] = useState(new Date());
    const [results, setResults] = useState(null);  // State to hold the problem results
    const [error, setError] = useState(null);

    // Fetch the results of the problem submission when the component is loaded
    useEffect(() => {
        if (submissionId) {
            fetchResults(submissionId);
        }
    }, [submissionId]);

    // Fetch results from the API
    const fetchResults = async (submissionId) => {
        try {
            const response = await fetch(`http://localhost:8005/get-results/${submissionId}/`, {
                method: 'GET'
            });

            if (!response.ok) {
                throw new Error(`Failed to fetch results: ${response.statusText}`);
            }

            const data = await response.json();
            setResults(data);  // Set the results in the state
        } catch (error) {
            setError(`Error fetching results: ${error.message}`);
        }
    };

    // Set interval to update the current time every second
    useEffect(() => {
        const timer = setInterval(() => {
            setCurrentDateTime(new Date());
        }, 1000);

        return () => {
            clearInterval(timer);
        };
    }, []);

    // Render a chart if the results have data to visualize (optional)
    useEffect(() => {
        if (results && results.stats) {
            const ctx = document.getElementById('results-chart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: Object.keys(results.stats),  // Assuming results.stats is an object
                    datasets: [{
                        label: 'Result Stats',
                        data: Object.values(results.stats),
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }
    }, [results]);

    return (
        <div className="landing">
            <img src={logo2} alt="solveMe Logo" className="top-logo" />
            <h1>Problem Results</h1>
            <div className="top-section">
                <div className="username-display">
                    <strong>Welcome, {username}</strong>
                </div>
                <div className="date-time-box">
                    {currentDateTime.toLocaleDateString()} {currentDateTime.toLocaleTimeString()}
                </div>
            </div>

            <div className="results-container">
                {error ? (
                    <p>{error}</p>
                ) : results ? (
                    <div>
                        <h2>Results for Submission ID: {submissionId}</h2>
                        <pre>{JSON.stringify(results, null, 2)}</pre>  {/* Display the raw results data */}
                        <canvas id="results-chart" width="400" height="400"></canvas>  {/* Chart for visualizing results */}
                    </div>
                ) : (
                    <p>Loading results...</p>
                )}
            </div>
        </div>
    );
}

export default ResultsPage;

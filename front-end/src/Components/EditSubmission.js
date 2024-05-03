import React, { useState, useEffect } from 'react';
import '../index.css';
import logo2 from '../../src/topLogo.png';
import graph1 from '../../src/graph1.png';
import graph2 from '../../src/graph2.png';
import { useLocation, useNavigate } from 'react-router-dom';

function EditSubmission() {
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
        { name:"I AM", type: 'type 1', description: "he wanted to be HIM", value: "1000$" },
        { name:"I AM NOT", type:'type 2' ,description: "he did not want to be HIM", value: "2500$" },
        // ... other submissions
    ];

    // Add any functionality for when the "New Problem" button is clicked
    const handleNewClick = () => {
        navigate('/NewSubmission', { state: { username: username } }); // Navigate and pass username
    };

    return (
        <div className="landing">
            <img src={logo2} alt="solveMe Logo" className="top-logo"/>
            <h1>View/Edit Submission </h1>
            <div className="top-section">
                <div className="username-display">
                    <strong>status(username,company,account status, logout)</strong>
                </div>
                <div className="date-time-box">
                    {currentDateTime.toLocaleDateString()} {currentDateTime.toLocaleTimeString()}
                </div>
            </div>
            <div className="submissions-table">
                <table>
                    <thead>
                    <tr>
                        <th>submission id</th>
                        <th>submission name</th>
                        <th>solver id</th>
                        <th>creator</th>
                        <th>createdOn</th>
                        <th>status</th>
                    </tr>
                    </thead>

                </table>
            </div>

            <div className="submissions-table">
                <table>
                    <thead>
                    <td>Metadata</td>
                    <tr>
                        <th>Name</th>
                        <th>Type</th>
                        <th>Value</th>
                        <th>Description</th>

                    </tr>
                    </thead>
                    <tbody>
                    {submissions.map((submission, index) => (
                        <tr key={index}>
                            <td>{submission.name}</td>
                            <td>{submission.type}</td>
                            <td>{submission.value}</td>
                            <td>{submission.description}</td>
                        </tr>
                    ))}
                    </tbody>
                </table>

            </div>

            <div className="submissions-table">
                <table>
                    <thead>
                    <tr>
                        <th colSpan="2">Dataset</th>
                        <th>Graph</th>
                        <th>Template</th>
                        <th>Upload</th>
                        <th>Download</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr>
                        <td colSpan="2">Dataset 1</td>
                        <td><img src={graph1} alt="Graph 1"/></td>
                        <td>
                            <button>Template</button>
                        </td>
                        <td>
                            <button>Upload</button>
                        </td>
                        <td>
                            <button>Download</button>
                        </td>
                    </tr>
                    <tr>
                        <td colSpan="2">Dataset 2</td>
                        <td><img src={graph2} alt="Graph 2"/></td>
                        <td>
                            <button>Template</button>
                        </td>
                        <td>
                            <button>Upload</button>
                        </td>
                        <td>
                            <button>Download</button>
                        </td>
                    </tr>
                    <tr>
                        <td colSpan="2">Dataset 3</td>
                        <td>
                            <div className="drop-area">Drag file to upload</div>
                        </td>
                        <td>
                            <button>Template</button>
                        </td>
                        <td>
                            <button>Upload</button>
                        </td>
                        <td>
                            <button disabled>Download</button>
                        </td>
                    </tr>
                    </tbody>
                </table>
                <button className="create-button">Done</button>
            </div>




        </div>
    );
}

export default EditSubmission;
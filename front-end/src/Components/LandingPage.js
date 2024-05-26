// src/Components/LandingPage.js
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import '../index.css';
import logo from '../../src/solveMe-Logo.png';
import logo2 from '../../src/topLogo.png';
import ButtonGroup from './ButtonGroup';

function LandingPage() {
    const [currentDateTime, setCurrentDateTime] = useState(new Date());

    useEffect(() => {
        const timer = setInterval(() => {
            setCurrentDateTime(new Date());
        }, 1000);

        return () => {
            clearInterval(timer);
        };
    }, []);

    return (
        <div className="landing">
            <img src={logo2} alt="solveMe Logo" className="top-logo"/>
            <h1>Welcome to SolveMe!</h1>
            <div className="top-section">
                <div className="navigation-buttons">
                    <Link to="/signup" className="btn btn-primary">Sign Up</Link>
                    <Link to="/login" className="btn btn-secondary">Login</Link>
                </div>
                <div className="date-time-box">
                    {currentDateTime.toLocaleDateString()} {currentDateTime.toLocaleTimeString()}
                </div>
            </div> {/* This closes the .top-section div */}
            <img src={logo} alt="solveMe Logo" className="center-logo"/>
            <ButtonGroup />
        </div>
    );
}
//<Link to="/AllSubmissions" className="btn btn-secondary">Admin</Link>
export default LandingPage;

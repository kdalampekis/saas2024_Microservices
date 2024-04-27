import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../index.css';
import logo from '../../src/solveMe-Logo.png';
import logo2 from '../../src/topLogo.png';
import LoginGroup from './loginbuttons';

function LoginForm() {
    const navigate = useNavigate(); // Use useNavigate for navigation
    const [form, setForm] = useState({
        username: '',
        password: ''
    });

    const handleChange = (event) => {
        const { name, value } = event.target;
        setForm(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        console.log('Login Attempt:', form);
        // Here you might add code to validate credentials via an API call
        navigate('/MySubmissions', { state: { username: form.username } }); // Pass username in navigation state
    };

    const [currentDateTime, setCurrentDateTime] = useState(new Date()); // State for the current date/time

    useEffect(() => {
        const timer = setInterval(() => {
            setCurrentDateTime(new Date()); // Update time every second
        }, 1000);

        return () => clearInterval(timer); // Clear interval on component unmount
    }, []);

    return (
        <div className="landing">
            <img src={logo2} alt="solveMe Logo" className="top-logo" />
            <h1>Login!</h1>
            <div className="top-section">
                <div className="navigation-buttons">
                    <Link to="/signup" className="btn btn-primary">Sign Up</Link>
                    <Link to="/login" className="btn btn-secondary">Login</Link>
                </div>
                <div className="date-time-box">
                    {currentDateTime.toLocaleDateString()} {currentDateTime.toLocaleTimeString()}
                </div>
            </div>
            <img src={logo} alt="solveMe Logo" className="center-logo" />
            <LoginGroup form={form} onChange={handleChange} onSubmit={handleSubmit} />
        </div>
    );
}

export default LoginForm;

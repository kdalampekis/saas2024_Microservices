import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../index.css';
import logo from '../../src/solveMe-Logo.png';
import logo2 from '../../src/topLogo.png';
import LoginGroup from './loginbuttons';

function LoginForm() {
    const navigate = useNavigate();
    const [form, setForm] = useState({
        username: '',
        password: ''
    });
    const [error, setError] = useState('');

    const handleChange = (event) => {
        const { name, value } = event.target;
        setForm(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        console.log('Login Attempt:', form);

        try {
            const response = await fetch('http://localhost:8007/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(form),
            });

            if (!response.ok) {
                throw new Error('Login failed');
            }

            const data = await response.json();
            console.log('Login Success:', data);

            // Check if the token exists in the response
            if (!data.token) {
                throw new Error('Token not found in login response');
            }

            // Store the token in localStorage
            localStorage.setItem('token', data.token);
            console.log('Stored token:', localStorage.getItem('token'));

            // Redirect based on user type
            if (data.is_superuser) {
                navigate('/allsubmissions', { state: { username: form.username } });
            } else {
                navigate('/MySubmissions', { state: { username: form.username } });
            }
        } catch (error) {
            console.error('Error:', error);
            setError('Invalid username or password');
        }
    };


    const handleGoogleLogin = () => {
        // Redirect to the backend Google login URL
        window.location.href = 'http://localhost:8007/accounts/login/google-oauth2/';
    };

    const [currentDateTime, setCurrentDateTime] = useState(new Date());

    useEffect(() => {
        const timer = setInterval(() => {
            setCurrentDateTime(new Date());
        }, 1000);

        return () => clearInterval(timer);
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
            {error && <div className="error-message">{error}</div>}
            <LoginGroup form={form} onChange={handleChange} onSubmit={handleSubmit} />
            <button onClick={handleGoogleLogin} className="btn btn-google">Login with Google</button>
        </div>
    );
}

export default LoginForm;
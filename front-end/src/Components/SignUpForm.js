import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function SignUpForm() {
    const [form, setForm] = useState({
        username: '',
        email: '',
        password: ''
    });
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const navigate = useNavigate();

    const handleChange = (event) => {
        const { name, value } = event.target;
        setForm(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        console.log('User Registration Attempt:', form);

        try {
            const response = await fetch('http://localhost:8007/signup/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(form),
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.detail || 'Signup failed');
            }

            const data = await response.json();
            console.log('Registration Success:', data);
            setSuccess('Registration successful! Please log in.');
            setError('');
    

            setTimeout(() => {
                navigate('/login');
            }, 2000);
        } catch (error) {
            console.error('Error:', error);
            setError(error.message || 'Registration failed. Please try again.');
            setSuccess('');
        }
    };

    return (
        <div className="sign-up-form">
            <h1>Sign Up</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>
                        Username:
                        <input
                            type="text"
                            name="username"
                            value={form.username}
                            onChange={handleChange}
                        />
                    </label>
                </div>
                <div>
                    <label>
                        Email:
                        <input
                            type="email"
                            name="email"
                            value={form.email}
                            onChange={handleChange}
                        />
                    </label>
                </div>
                <div>
                    <label>
                        Password:
                        <input
                            type="password"
                            name="password"
                            value={form.password}
                            onChange={handleChange}
                        />
                    </label>
                </div>
                <button type="submit">Sign Up</button>
            </form>
            {error && <div className="error-message">{error}</div>}
            {success && <div className="success-message">{success}</div>}
        </div>
    );
}

export default SignUpForm;
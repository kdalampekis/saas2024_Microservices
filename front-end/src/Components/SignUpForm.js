// src/Components/SignUpForm.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function SignUpForm() {
    const [form, setForm] = useState({
        username: '',
        email: '',
        password: ''
    });
    const navigate = useNavigate(); // useNavigate replaces useHistory

    const handleChange = (event) => {
        const { name, value } = event.target;
        setForm(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        console.log('User Registered:', form);
        navigate('/login'); // navigate replaces history.push
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
        </div>
    );
}

export default SignUpForm;

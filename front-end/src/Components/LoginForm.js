// src/LoginForm.js
import React, { useState } from 'react';

function LoginForm() {
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
        // Here you might send a request to the backend to validate user credentials
    };

    return (
        <div className="login-form">
            <h1>Login</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>
                        Username:
                        <input
                            type="text"
                            name="username"
                            value={form.username}
                            onChange={handleChange}
                            required
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
                            required
                        />
                    </label>
                </div>
                <button type="submit">Login</button>
            </form>
        </div>
    );
}

export default LoginForm;

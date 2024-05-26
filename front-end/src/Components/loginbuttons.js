// LoginGroup.js
import React from 'react';

function LoginGroup({ form, onChange, onSubmit }) {
    return (
        <div className="login-group">
            <form className="login-form" onSubmit={onSubmit}>
                <div className="form-group">
                    <label htmlFor="username">Username:</label>
                    <input
                        type="text"
                        id="username"
                        name="username"
                        className="form-input"
                        value={form.username}
                        onChange={onChange}
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="password">Password:</label>
                    <input
                        type="password"
                        id="password"
                        name="password"
                        className="form-input"
                        value={form.password}
                        onChange={onChange}
                    />
                </div>
                <button type="submit" className="btn btn-primary">Login</button>
            </form>
        </div>
    );
}

export default LoginGroup;
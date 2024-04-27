// LoginGroup.js
import React from 'react';

function LoginGroup() {
    return (
        <div className="login-group">
            <form className="login-form">
                <div className="form-group">
                    <label htmlFor="username">Username:</label>
                    <input type="text" id="username" name="username" className="form-input" />
                </div>
                <div className="form-group">
                    <label htmlFor="password">Password:</label>
                    <input type="password" id="password" name="password" className="form-input" />
                </div>
                <button type="submit" className="btn btn-primary">Login</button>
            </form>
        </div>
    );
}

export default LoginGroup;

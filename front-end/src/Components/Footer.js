// src/Components/Footer.js
import React from 'react';
import '../index.css'; // assuming your styles are here

const Footer = () => {
    return (
        <footer className="app-footer">
            <p>&copy; {(new Date().getFullYear())} solveMe. All rights reserved.</p>
            <p>Use our application responsibly and solve your problems today!</p>
        </footer>
    );
};

export default Footer;

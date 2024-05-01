// src/Components/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import '../App.css'; // Make sure this path is correct
import LandingPage from './LandingPage';
import SignUpForm from './SignUpForm';
import LoginForm from './LoginForm';
import Footer from './Footer';
import MySubmissions from "./MySubmissions";
import NewSubmission from "./NewSubmission";

function App() {
    return (
        <Router>
            <div className="App">
                <header className="App-header">
                    {/*
                    <nav>
                        <Link to="/">Home</Link> |
                        <Link to="/signup">Sign Up</Link> |
                        <Link to="/login">Login</Link>
                    </nav>
                    */}
                    <Routes>
                        <Route path="/" element={<LandingPage />} />
                        <Route path="/signup" element={<SignUpForm />} />
                        <Route path="/login" element={<LoginForm />} />
                        <Route path="/MySubmissions" element={<MySubmissions />} />
                        <Route path="/mySubmissions" element={<MySubmissions username="UsernameHere" />} />
                        <Route path="/MySubmissions" element={<MySubmissions />} />
                        <Route path="/NewSubmission" element={<NewSubmission />} />
                    </Routes>
                </header>
                <Footer />
            </div>
        </Router>
    );
}

export default App;

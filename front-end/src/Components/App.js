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
import AllSubmissions from "./AllSubmissions";
import ViewSubmissionResults from "./ViewSubmissionResults";

function App() {
    return (
        <Router>
            <div className="App">
                <header className="App-header">
                    {/*
                    <nav>
                        <Link to="/">Home Alone</Link> |
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
                        <Route path="/AllSubmissions" element={<AllSubmissions />} />
                        <Route path="/ViewSubmissionResults" element={<ViewSubmissionResults />} />
                    </Routes>
                </header>
                <Footer />
            </div>
        </Router>
    );
}

export default App;

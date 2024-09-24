import React, { useState, useEffect } from 'react';
import '../index.css'; // Ensure your CSS file includes the necessary styles
import logo2 from '../../src/topLogo.png';
import { useLocation, useNavigate } from 'react-router-dom';

function ViewSubmissionResults() {
  const location = useLocation();
  const navigate = useNavigate();

  // Use fallback values in case state is undefined
  const username = location.state?.username || 'Guest';
  const submissionId = location.state?.submissionId;

  console.log("submissionId:", submissionId);

  const [currentDateTime, setCurrentDateTime] = useState(new Date());
  const [metadata, setMetadata] = useState(null);     // Store the metadata
  const [resultData, setResultData] = useState(null); // Store the resultData
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentDateTime(new Date());
    }, 1000);

    return () => {
      clearInterval(timer);
    };
  }, []);

  // Fetch submission data
  useEffect(() => {
    if (!submissionId) {
      setError('Submission ID not provided');
      setLoading(false);
      return;
    }

    const fetchSubmissionData = async () => {
      try {
        setLoading(true);
        const url = `http://localhost:8005/get-results/${submissionId}/`;
        console.log("Fetching URL:", url);
        const response = await fetch(url);

        if (!response.ok) {
          throw new Error(`Failed to fetch results: ${response.statusText}`);
        }

        const fetchedData = await response.json();
        console.log("Fetched data:", fetchedData);

        // Set the metadata and resultData fields
        setMetadata(fetchedData.submission_data.metadata);
        setResultData(fetchedData.result_data);
      } catch (error) {
        console.error("Error fetching submission results:", error);
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    fetchSubmissionData();
  }, [submissionId]);

  const handleReturnClick = () => {
    navigate('/MySubmissions', { state: { username } });
  };

  // Recursive component to render JSON data with collapsible sections
  const JsonRenderer = ({ data, level = 0 }) => {
    const [collapsed, setCollapsed] = useState(false);

    if (typeof data === 'object' && data !== null) {
      if (Array.isArray(data)) {
        return (
          <div className="json-item" style={{ marginLeft: level * 20 }}>
            <div className="json-collapsible" onClick={() => setCollapsed(!collapsed)}>
              <span className="json-toggle">{collapsed ? '+' : '-'}</span>
              <span className="json-key">Array [{data.length}]</span>
            </div>
            {!collapsed && (
              <div className="json-children">
                {data.map((item, index) => (
                  <JsonRenderer key={index} data={item} level={level + 1} />
                ))}
              </div>
            )}
          </div>
        );
      } else {
        return (
          <div className="json-item" style={{ marginLeft: level * 20 }}>
            <div className="json-collapsible" onClick={() => setCollapsed(!collapsed)}>
              <span className="json-toggle">{collapsed ? '+' : '-'}</span>
              <span className="json-key">Object</span>
            </div>
            {!collapsed && (
              <div className="json-children">
                {Object.entries(data).map(([key, value]) => (
                  <div key={key} className="json-item">
                    <span className="json-key" style={{ marginLeft: (level + 1) * 20 }}>
                      {key}:
                    </span>
                    <JsonRenderer data={value} level={level + 1} />
                  </div>
                ))}
              </div>
            )}
          </div>
        );
      }
    } else {
      // Render primitive values with syntax highlighting
      let valueStyle = 'json-primitive';
      if (typeof data === 'string') {
        valueStyle = 'json-string';
      } else if (typeof data === 'number') {
        valueStyle = 'json-number';
      } else if (typeof data === 'boolean') {
        valueStyle = 'json-boolean';
      } else if (data === null) {
        valueStyle = 'json-null';
      }

      return (
        <span className={`json-value ${valueStyle}`}>
          {typeof data === 'string' ? `"${data}"` : String(data)}
        </span>
      );
    }
  };

  return (
    <div className="landing">
      <img src={logo2} alt="solveMe Logo" className="top-logo" />
      <h1>View Submission Results</h1>
      <div className="top-section">
        <div className="username-display">
          <strong>Status: {username}</strong>
        </div>
        <div className="date-time-box">
          {currentDateTime.toLocaleDateString()} {currentDateTime.toLocaleTimeString()}
        </div>
      </div>

      {loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p>Error: {error}</p>
      ) : (
        <>
          {metadata && (
            <>
              <h2>Metadata</h2>
              <div className="json-container">
                <JsonRenderer data={metadata} />
              </div>
            </>
          )}
          {resultData && (
            <>
              <h2>Result Data</h2>
              <div className="json-container">
                <JsonRenderer data={resultData} />
              </div>
            </>
          )}
        </>
      )}

      <div className="button-group">
        <button className="non-functional-btn">Download Excel</button>
        <button className="non-functional-btn">Download Raw</button>
        <button className="non-functional-btn" onClick={handleReturnClick}>Return</button>
      </div>
    </div>
  );
}

export default ViewSubmissionResults;

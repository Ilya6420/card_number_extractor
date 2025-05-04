import React, { useEffect, useState } from 'react';
import './App.css';
import ImageUploader from './components/ImageUploader';
import api from './services/api';

function App() {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const checkApiHealth = async () => {
      try {
        const isHealthy = await api.checkHealth();
        if (!isHealthy) {
          throw new Error('Unable to connect to the API service. Please make sure the backend server is running.');
        }
        setIsLoading(false);
      } catch (error) {
        setError(error.message);
        setIsLoading(false);
      }
    };

    checkApiHealth();
  }, []);

  if (isLoading) {
    return (
      <div className="app-container">
        <div className="loading-state">
          <div className="spinner" />
          <p>Checking service availability...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app-container">
        <div className="error-state">
          <h2>Service Unavailable</h2>
          <p>{error}</p>
          <div className="error-actions">
            <button onClick={() => window.location.reload()}>
              Try Again
            </button>
            <p className="error-hint">
              Make sure the backend server is running at {process.env.REACT_APP_API_URL || 'http://localhost:8000'}
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-content">
          <h1>Bank Card Number Extractor</h1>
          <p className="header-description">Upload an image of a bank card to extract the card number</p>
        </div>
      </header>
      
      <main className="app-main">
        <div className="main-content">
          <ImageUploader />
        </div>
      </main>
    </div>
  );
}

export default App;

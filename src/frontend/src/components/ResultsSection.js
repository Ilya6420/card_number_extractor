import React from 'react';
import PropTypes from 'prop-types';
import './ResultsSection.css';

const ResultsSection = ({ mlResult, showBboxes, onToggleBboxes, onDownload }) => {
  if (!mlResult) return null;

  return (
    <div className="result-section">
      <h3>Analysis Results</h3>
      <p>Prediction: {mlResult.card_number.replace(/(\d{4})(?=\d)/g, '$1 ')}</p>
      <p>Bbox: {JSON.stringify(mlResult.bbox, null, 2)}</p>
      <p>Confidence: {(mlResult.confidence * 100).toFixed(2)}%</p>
      <div className="button-group">
        <button 
          onClick={onToggleBboxes}
          className="bbox-button"
          aria-pressed={showBboxes}
        >
          {showBboxes ? 'Hide Bboxes' : 'Show Bboxes'}
        </button>
        <button 
          onClick={onDownload}
          className="download-button"
        >
          Download Extractor Results
        </button>
      </div>
    </div>
  );
};

ResultsSection.propTypes = {
  mlResult: PropTypes.shape({
    card_number: PropTypes.string.isRequired,
    bbox: PropTypes.arrayOf(PropTypes.arrayOf(PropTypes.number)).isRequired,
    confidence: PropTypes.number.isRequired,
  }),
  showBboxes: PropTypes.bool.isRequired,
  onToggleBboxes: PropTypes.func.isRequired,
  onDownload: PropTypes.func.isRequired,
};

export default ResultsSection; 
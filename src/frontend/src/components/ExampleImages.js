import React, { useState } from 'react';
import PropTypes from 'prop-types';
import './ExampleImages.css';

const ExampleImages = ({ exampleImages, onImageSelect }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className={`examples-section ${isExpanded ? 'expanded' : 'collapsed'}`}>
      <h3>
        Example Images for Testing
        <button 
          className="toggle-button"
          onClick={() => setIsExpanded(!isExpanded)}
          aria-expanded={isExpanded}
        >
          {isExpanded ? 'Collapse' : 'Expand'}
        </button>
      </h3>
      <p>Click on any example image below to test the extractor:</p>
      <div className="example-images">
        {exampleImages.map((example, index) => (
          <div key={index} className="example-image-container">
            <img
              src={example.url}
              alt={example.description}
              onClick={() => onImageSelect(example.url)}
              className="example-image"
              role="button"
              tabIndex="0"
              onKeyPress={(e) => e.key === 'Enter' && onImageSelect(example.url)}
            />
            <p className="example-description">{example.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

ExampleImages.propTypes = {
  exampleImages: PropTypes.arrayOf(
    PropTypes.shape({
      url: PropTypes.string.isRequired,
      description: PropTypes.string.isRequired,
    })
  ).isRequired,
  onImageSelect: PropTypes.func.isRequired,
};

export default ExampleImages; 
import React, { useState } from 'react';
import './ImageUploader.css';
import example1 from '../examples/card_1118_full.png';
import example2 from '../examples/photo_2025-05-04_01-39-26.jpg';
import example3 from '../examples/Screenshot 2025-04-16 181426.png';
import api from '../services/api';
import ExampleImages from './ExampleImages';
import ImagePreview from './ImagePreview';
import ResultsSection from './ResultsSection';

const ImageUploader = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [mlResult, setMlResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showBboxes, setShowBboxes] = useState(false);

  const exampleImages = [
    {
      url: example1,
      description: 'Example 1: Synthetic Card Image'
    },
    {
      url: example2,
      description: 'Example 2: Real Card Image'
    },
    {
      url: example3,
      description: 'Example 3: Background and Noise'
    }
  ];

  const handleExampleClick = async (imageUrl) => {
    try {
      const response = await fetch(imageUrl);
      const blob = await response.blob();
      const reader = new FileReader();
      
      reader.onloadend = () => {
        setSelectedImage(reader.result);
        setError(null);
        setMlResult(null);
        setShowBboxes(false);
      };
      
      reader.readAsDataURL(blob);
    } catch (error) {
      console.error('Error loading example image:', error);
      setError('Failed to load example image');
    }
  };

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setSelectedImage(reader.result);
        setError(null);
        setMlResult(null);
        setShowBboxes(false);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async () => {
    if (!selectedImage) return;
    
    setIsLoading(true);
    setError(null);
    
    try {
      const base64Data = selectedImage.split(',')[1];
      const blob = await fetch(`data:image/jpeg;base64,${base64Data}`).then(res => res.blob());
      const result = await api.predictCardNumber(blob);
      setMlResult(result);
    } catch (error) {
      console.error('Error processing image:', error);
      setError(error.message || 'Failed to process image. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownload = () => {
    if (!mlResult) return;
    
    const dataStr = JSON.stringify(mlResult, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = 'analysis_result.json';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="image-uploader-container">
      {/* <h2>Bank Card Number Extractor</h2> */}
      
      <ExampleImages 
        exampleImages={exampleImages}
        onImageSelect={handleExampleClick}
      />

      <div className="upload-section">
        <input
          type="file"
          accept="image/*"
          onChange={handleImageUpload}
          className="file-input"
          aria-label="Upload image"
        />
        
        {selectedImage && (
          <ImagePreview
            imageUrl={selectedImage}
            bbox={mlResult?.bbox}
            showBboxes={showBboxes}
          />
        )}
      </div>

      {selectedImage && (
        <button 
          onClick={handleSubmit} 
          disabled={isLoading}
          className="submit-button"
        >
          {isLoading ? 'Processing...' : 'Extract Card Number'}
        </button>
      )}

      {error && (
        <div className="error-message" role="alert">
          {error}
        </div>
      )}

      <ResultsSection
        mlResult={mlResult}
        showBboxes={showBboxes}
        onToggleBboxes={() => setShowBboxes(!showBboxes)}
        onDownload={handleDownload}
      />
    </div>
  );
};

export default ImageUploader; 
import React, { useRef, useEffect } from 'react';
import PropTypes from 'prop-types';
import './ImagePreview.css';

const ImagePreview = ({ imageUrl, bbox, showBboxes }) => {
  const canvasRef = useRef(null);
  const imageRef = useRef(null);

  const drawBboxes = () => {
    if (!canvasRef.current || !imageRef.current || !bbox) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const image = imageRef.current;
    
    // Get the actual displayed dimensions of the image
    const displayedWidth = image.offsetWidth;
    const displayedHeight = image.offsetHeight;
    
    // Set canvas size to match displayed image dimensions
    canvas.width = displayedWidth;
    canvas.height = displayedHeight;
    
    // Calculate scaling factors
    const scaleX = displayedWidth / image.naturalWidth;
    const scaleY = displayedHeight / image.naturalHeight;
    
    // Clear previous drawings
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw the bbox using scaled coordinates
    ctx.strokeStyle = '#00ff00';
    ctx.lineWidth = 2;
    ctx.beginPath();
    bbox.forEach(([x, y], idx) => {
      const scaledX = x * scaleX;
      const scaledY = y * scaleY;
      if (idx === 0) {
        ctx.moveTo(scaledX, scaledY);
      } else {
        ctx.lineTo(scaledX, scaledY);
      }
    });
    // Close the shape by connecting last point to the first
    if (bbox.length > 0) {
      const [x0, y0] = bbox[0];
      ctx.lineTo(x0 * scaleX, y0 * scaleY);
    }
    ctx.stroke();
  };

  useEffect(() => {
    if (showBboxes) {
      drawBboxes();
    } else if (canvasRef.current) {
      const ctx = canvasRef.current.getContext('2d');
      ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
    }
  }, [showBboxes, bbox]);

  return (
    <div className="image-preview">
      <img 
        ref={imageRef}
        src={imageUrl} 
        alt="Selected" 
        style={{ position: 'relative' }}
      />
      <canvas
        ref={canvasRef}
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          pointerEvents: 'none'
        }}
      />
    </div>
  );
};

ImagePreview.propTypes = {
  imageUrl: PropTypes.string.isRequired,
  bbox: PropTypes.arrayOf(PropTypes.arrayOf(PropTypes.number)),
  showBboxes: PropTypes.bool.isRequired,
};

export default ImagePreview; 
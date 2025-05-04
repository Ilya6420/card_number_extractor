// API Configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// API Service
const api = {
  /**
   * Predict card number from image
   * @param {File} imageFile - The image file to process
   * @returns {Promise<Object>} - The prediction result
   * @throws {Error} - If the request fails
   */
  predictCardNumber: async (imageFile) => {
    try {
      const formData = new FormData();
      formData.append('file', imageFile, 'image.jpg');

      const response = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
      }

      return response.json();
    } catch (error) {
      console.error('API Error:', error);
      throw new Error(error.message || 'Failed to process image. Please try again.');
    }
  },

  /**
   * Check if the API is available
   * @returns {Promise<boolean>} - True if the API is available
   */
  checkHealth: async () => {
    try {
      // Try to connect to the API base URL
      const response = await fetch(API_BASE_URL);
      return response.ok;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  }
};

export default api; 
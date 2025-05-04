# Card Number Extractor API

A FastAPI application that extracts card numbers from images.

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Run the application using:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `GET /`: Health check endpoint
- `POST /predict`: Extract card number from an image

### Card Number Extraction Endpoint

Send a POST request to `/predict` with an image file in the request body using form-data with the key `file`.

Example using curl:
```bash
curl -X POST "http://localhost:8000/predict" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@path/to/your/image.jpg"
```

The response will be:
```json
{
    "card_number": "1234567890123456",
    "bbox": [x1, y1, x2, y2],
    "confidence": 0.95
}
```

If no valid card number is found, the API will return a 400 status code with an error message.

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development

For development purposes, you can install additional development dependencies:
```bash
pip install -r requirements-dev.txt
```

The project includes:
- Pre-commit hooks for code quality
- Flake8 configuration for linting
- Type checking and code formatting tools
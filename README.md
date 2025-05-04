# Bank Card Number Extractor

A full-stack application for extracting and analyzing bank card numbers from images using a machine learning backend and a modern React frontend.

## Table of Contents
- [Project Structure](#project-structure)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Backend Setup](#backend-setup-fastapi)
  - [Frontend Setup](#frontend-setup-react)
- [Usage](#usage)
- [Folder Details](#folder-details)
- [Stages](#stages)
  - [Data Collection and Preparation](#data-collection-and-preparation)
  - [Labelling](#labelling)
  - [Pre-processing](#pre-processing)
  - [Training](#training)
  - [Infrence](#infrence)
  - [Storage of Artifacts](#storage-of-artifacts)
- [Future System Improvements](#future-system-improvements)
  - [Current Implementation Version](#current-implementation-version)
  - [Improved Version](#improved-version)

---

## Project Structure

```
FrontPoint/
├── src/
│   ├── backend/      # FastAPI backend for ML inference
│   ├── frontend/     # React frontend for user interaction
│   └── ai/           # Machine learning and data processing
│       ├── notebooks/    # Jupyter notebooks
│       ├── data/         # Training and test datasets
│       ├── backgrounds/  # Background images for data generation
│       └── fonts/        # Font files for synthetic data generation
├── architecture/     # System architecture diagrams and documentation
```

---

## Features

- Upload images of bank cards via a user-friendly web interface
- Extract and visualize card numbers and bounding boxes using ML
- Download analysis results as JSON

---

## Getting Started

### Prerequisites

- Node.js (v22.14.0)
- Python 3.10

---

## Backend Setup (FastAPI)

1. **Navigate to the backend directory:**
   ```bash
   cd src/backend
   ```

2. **Create and activate a conda environment (recommended):**
   ```bash
   conda create -n <venv_name> python=3.10
   conda activate <venv_name>
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the backend server:**
   ```bash
   uvicorn main:app --reload
   ```
   The backend will be available at `http://localhost:8000`.

---

## Frontend Setup (React)

1. **Navigate to the frontend directory:**
   ```bash
   cd src/frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the frontend development server:**
   ```bash
   npm start
   ```
   The frontend will be available at `http://localhost:3000`.

---

## Usage

1. Open the frontend in your browser.
2. Upload an image of a bank card.
3. Click "Extract Card Number" to analyze the image.
4. View the extracted card number, bounding box, and confidence.
5. Optionally, show bounding boxes on the image or download the results as a JSON file.

---

## Folder Details

- **src/backend/**: FastAPI backend, ML model inference, API endpoints.
- **src/frontend/**: React app, UI components, image upload, result visualization.

---

# Stages
## Data Collection and Preparation
1. No public/open datasets were used.
2. A synthetic data generation pipeline was implemented: ```src/ai/notebooks/credit_card_generator.ipynb```.

**Note**: The generator currently creates only the card images without any background or contextual elements. This can be improved in future iterations.

## Labelling
1. Since the data is synthetically generated, we automatically obtain bounding boxes and class labels.

## Pre-processing
1. Standard appearance normalization, augmentation, and post-processing are supported via PaddleOCR's pipeline.

## Training
1. The training phase was skipped due to time constraints and a limited amount of high-quality data.

## Infrence
1. Backend: Implemented using FastAPI with PaddleOCR (PP-OCRv4 pre-trained model) as the inference engine.
2. Frontend: A lightweight UI was developed for quick interaction and testing.

## Storage of Artifacts
1. Not implemented in the current version.

## Future System Improvements

### Current Implementation Version
![Current Version](architecture/Bank%20Card%20Number%20Extractor%20-%20V1.png)

#### Version 1 - Baseline PoC pipeline
| Component | Implementation | Rationale |
|-----------|----------------|-----------|
| 📸 **Data Creation** | Custom Synthetic Generation | Real card data is sensitive; synthetic images mimic card numbers |
| 🏷️ **Data Labeling** | Scripted Auto-labeling | Quick bootstrap with synthetic bounding boxes and classes |
| 🖥️ **Training** | Kaggle Notebooks | Free GPU resources with minimal setup overhead |
| 🌐 **Deployment** | Basic Frontend + Backend | Minimal UI to demonstrate predictions |

### Improved Version
![Current Version](architecture/Bank%20Card%20Number%20Extractor%20-%20V2.png)

#### Version 2 - Improved MVP Pipeline
| Component | Implementation | Improvement | Benefit |
|-----------|----------------|-------------|---------|
| 📸 **Data Creation** | Virtual Machines + LLMs | Scalable, isolated compute | Better diversity and realism in generated data |
| 💾 **Storage** | MinIO (S3-Like) | Centralized, scalable storage | Standardized access from all pipeline stages |
| 🏷️ **Annotation** | Label Studio | UI-based, human-in-the-loop | Clean separation of labeling and storage |
| 🗄️ **Metadata** | PostgreSQL | Structured database | Enables queries, versioning, and reproducibility |
| 🧠 **Training** | MLflow + PaddleOCR | Standardized pipeline + tracking | Scalable, reproducible model lifecycle |
| 🚀 **Deployment** | Docker + FastAPI | Containerized inference | Easily deployable to cloud or on-premises |
| 🔄 **CI/CD** | Container Registry | Automated deployment | Reduced manual overhead, reliable versioning |

## Links and Licences

### PaddleOCR
- Repository: https://github.com/PaddlePaddle/PaddleOCR
- License: [Apache 2.0](https://github.com/PaddlePaddle/PaddleOCR?tab=Apache-2.0-1-ov-file#readme)

### Fonts
- Kredit Font: https://www.dafont.com/kredit.font
- License: [Creative Commons Zero](https://www.dafont.com/kredit.font#:~:text=Creative%20Commons%20Zero%20license)

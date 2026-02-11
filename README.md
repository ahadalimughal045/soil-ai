# Soil AI Analyzer 🌍🌱

A premium, AI-powered soil analysis tool that predicts soil composition and recommends crops based on image analysis.

## Features
- **Real-time Image Analysis**: Upload a soil sample image to get instant results.
- **Deep Insights**: Predicts Soil Type, Texture, pH levels (Min/Max), Nitrogen (N), Phosphorus (P), Potassium (K), and Organic Matter.
- **Climate Zone Detection**: Identifies the suitable climate zone for the soil sample.
- **Crop Recommendations**: Suggests the best crops to grow based on the soil health.
- **Premium UI**: Modern dark-themed interface with glassmorphism and smooth animations.

## Tech Stack
- **Frontend**: Vanilla HTML5, CSS3, JavaScript (ES6+).
- **Backend**: Python (FastAPI).
- **Processing**: PIL (Pillow) for image handling & simulated AI logic.

## How to Run

### 1. Start Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```
The backend will run at `http://localhost:8000`.

### 2. Start Frontend
Open `frontend/index.html` in your browser or serve it using any local server:
```bash
cd frontend
python -m http.server 3000
```
The frontend will be available at `http://localhost:3000`.

## Architecture
- `backend/main.py`: FastAPI server handling the `/analyze` POST endpoint.
- `frontend/`: Contains the static assets (HTML/CSS/JS).

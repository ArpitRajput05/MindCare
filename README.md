# 🧠 Mental Health Score Predictor

An interactive Machine Learning web application that predicts a student's mental health score (scale 0–10) based on lifestyle factors, daily screen time, social media platforms, sleep habits, and stress levels.

---

## 🚀 Features

- **Interactive UI**: Clean, responsive frontend with dynamic gauge visualizations.
- **Machine Learning Pipeline**: Random Forest Regressor trained with preprocessing (StandardScaler, OneHotEncoder, OrdinalEncoder, log transforms).
- **FastAPI Backend**: High-performance RESTful API with Pydantic request validation and interactive Swagger documentation at `/docs`.
- **Zero-Friction Local Run**: Double-click launcher (`run.bat`) or simple 1-line command.

---

## 📁 Project Structure

```text
Project3_Ltm/
├── Mental_Health_Model.pkl                  # Trained Machine Learning pipeline
├── Student Social Media And Mental Health Impact.csv  # Dataset
├── ML_Project.ipynb                         # Jupyter notebook for EDA & training
├── ML Project.html                          # Exported notebook report
├── main.py                                  # FastAPI server & endpoints
├── index.html                               # Frontend user interface
├── style.css                                # Styling and themes
├── script.js                                # Frontend logic & API calls
├── requirements.txt                         # Python dependencies
├── run.bat                                  # 1-click Windows runner
└── README.md                                # Documentation
```

---

## ⚡ Quick Start (How to Run Locally)

### Option 1: 1-Click Launch (Windows)
Simply double-click **`run.bat`** (or run `.\run.bat` in your terminal). It will launch the backend and automatically open `http://127.0.0.1:8000` in your web browser.

---

### Option 2: Using the Command Line

1. **Activate the virtual environment**:
   ```powershell
   .\.venv\Scripts\activate
   ```
   *(If creating fresh on another machine: `uv venv .venv` or `python -m venv .venv`, then `pip install -r requirements.txt`)*

2. **Start the FastAPI server**:
   ```powershell
   python main.py
   ```
   *Or via uvicorn directly:*
   ```powershell
   uvicorn main:app --reload
   ```

3. **Open in your browser**:
   Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📡 API Endpoints

- **`GET /`**: Serves the interactive web interface.
- **`GET /docs`**: Interactive Swagger API documentation and testing playground.
- **`POST /predict`**: Accepts student lifestyle features and returns the predicted mental health score (0–10).

### Sample Request:
```json
{
  "age": 21,
  "gender": "Male",
  "country": "India",
  "academic_level": "Undergraduate",
  "most_used_platform": "Instagram",
  "purpose_of_use": "Entertainment",
  "avg_daily_usage_hours": 4.5,
  "daily_unlocks": 60,
  "study_hours": 3.0,
  "physical_activity_hours": 1.0,
  "sleep_hours_per_night": 7.0,
  "stress_level": "Medium"
}
```

### Sample Response:
```json
{
  "predicted_mental_health_score": 6.36
}
```

---

## 📤 How to Push to Your Own GitHub Repository

Follow these 4 simple steps to upload this project to your GitHub:

1. **Initialize Git**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Mental Health Score ML application"
   ```

2. **Create a new repository on GitHub**:
   - Go to [github.com/new](https://github.com/new).
   - Name your repository (e.g., `mental-health-score`).
   - Do **NOT** initialize with README or .gitignore (we already have them).
   - Click **Create repository**.

3. **Link to your GitHub repository**:
   ```bash
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
   ```
   *(Replace with your actual GitHub username and repository name)*

4. **Push the code**:
   ```bash
   git push -u origin main
   ```

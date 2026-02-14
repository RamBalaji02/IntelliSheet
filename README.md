# IntelliSheet - AI Powered Spreadsheet Assistant

## Overview
IntelliSheet is a web application designed to enhance Excel usage by adding intelligent automation, smart filtering, voice commands, and automatic business insights.

## Tech Stack
- Frontend: Streamlit (Python)
- Backend: Python
- Libraries: pandas, openpyxl, matplotlib, speechrecognition
- Optional: SQLite for data storage

## Features
1. Smart Filtering System
2. Voice Command Support
3. Automatic Insight Generator
4. Smart Error Detection
5. Simple Automation Rules

## Project Structure
- `app.py`: Main Streamlit app (Controller) handling UI and user interactions
- `models/`: Backend modules (Model) encapsulating business logic
  - `filtering.py`: Implements smart filtering of dataframes based on conditions
  - `voice_commands.py`: Handles speech recognition and command parsing
  - `insights.py`: Generates automatic business insights from data
  - `error_detection.py`: Detects missing values and formula inconsistencies
  - `automation.py`: Contains automation rules and chart generation
- `views/`: Frontend UI components (View) (currently integrated in `app.py`)
- `data/`: Directory for uploaded and processed Excel files
- `static/`: Static assets (if any)

## Running Locally
1. Clone the repository:
```bash
git clone <repository-url>
cd IntelliSheet
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the app:
```bash
streamlit run app.py
```

5. Open the URL shown in the terminal (usually http://localhost:8501)

## Deployment

### Option 1: Streamlit Cloud (Recommended)
1. Push your code to a GitHub repository
2. Go to [Streamlit Cloud](https://share.streamlit.io/)
3. Click "New app" and connect your GitHub repository
4. Select the repository and branch, then specify `app.py` as the main file
5. Click "Deploy!"

### Option 2: Heroku
1. Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Log in to Heroku:
   ```bash
   heroku login
   ```
3. Create a new Heroku app:
   ```bash
   heroku create your-app-name
   ```
4. Deploy to Heroku:
   ```bash
   git add .
   git commit -m "Prepare for Heroku deployment"
   git push heroku main
   ```
5. Open the app:
   ```bash
   heroku open
   ```

### Option 3: Vercel
1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```
2. Deploy:
   ```bash
   vercel
   vercel --prod
   ```

## Future Upgrades
- Add React frontend for advanced UI
- Integrate more complex NLP for voice commands
- Add user authentication and history
- Support more file formats
- Deploy as a cloud service

---

This project is structured for beginner-friendly development with modular and scalable architecture following MVC pattern.

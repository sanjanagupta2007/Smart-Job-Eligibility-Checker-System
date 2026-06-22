# Smart Job Eligibility Checker System

A professional, feature-rich Web-based Placement Eligibility and Analytics System designed for engineering colleges. This system allows students to evaluate their readiness for campus placements, calculate their employability score, perform skill gap analysis, view visual analytics, download placement reports, and browse student records.

## 🚀 Key Features

1. **Placement Readiness Dashboard**: Shows total eligible companies, employability score (out of 100), and general placement readiness rating.
2. **Employability Score Calculator**: Computes a detailed score based on CGPA (35%), skills (35%), academic/personal projects (15%), and internships (15%).
3. **Company Eligibility Checker**: Evaluates student criteria against target companies (TCS, Infosys, Accenture, Wipro, Capgemini, Cognizant) and presents color-coded result cards with detailed rejection reasons.
4. **Skill Gap Analysis**: Identifies exact missing technical skills required by recruiters.
5. **Actionable Recommendations**: Suggests certifications, skills to learn, and specific areas of improvement.
6. **Data Visualizations**: Embeds Matplotlib-generated charts on the dashboard (Eligibility Donut, Score Breakdown, and Cohort comparison).
7. **Peer Directory (CSV Storage)**: Saves student records in a CSV database and allows reloading past student profiles directly into the form.
8. **Report Generator**: Generates and downloads a detailed, formatted plain-text assessment report (`.txt`).

---

## 🛠️ Technology Stack

- **Backend**: Python 3, Flask (REST APIs)
- **Data Handling**: Pandas (for CSV parsing and cohort processing)
- **Data Visualization**: Matplotlib (with memory-only `Agg` rendering backend)
- **Frontend**: HTML5, Vanilla CSS3 (modern glassmorphism UI & smooth transitions), JavaScript (Vanilla ES6)
- **Database**: Local CSV files (`database/companies.csv`, `database/students.csv`)

---

## 📂 Project Structure

```text
smart_job_eligibility_checker/
│
├── app.py                      # Flask backend server & endpoints
├── requirements.txt            # Python dependencies (flask, pandas, matplotlib)
├── README.md                   # Setup and execution guide
│
├── database/
│   ├── companies.csv           # Seed recruiter criteria database
│   └── students.csv            # Student profiles database
│
├── src/
│   ├── __init__.py             # Python package marker
│   ├── db_manager.py           # CSV database read/write actions
│   ├── analyzer.py             # Business calculations & rule engine
│   ├── charts.py               # Matplotlib graph engines
│   └── report.py               # Placement report builder
│
└── templates/
    └── index.html              # Modern, responsive single-page dashboard
```

---

## 💻 Setup and Execution

Follow these steps to run the application locally:

### 1. Prerequisite
Ensure you have **Python 3.8+** installed on your system.

### 2. Navigate to Project Directory
Open your command prompt or PowerShell and go to the project folder:
```bash
cd smart_job_eligibility_checker
```

### 3. Create & Activate Virtual Environment
Create a virtual environment to manage dependencies locally:
* **Windows (PowerShell)**:
  ```powershell
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  ```
* **macOS / Linux**:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 4. Install Dependencies
Run the installation command:
```bash
pip install -r requirements.txt
```

### 5. Launch the Server
Execute the Flask server:
```bash
python app.py
```

### 6. View in Browser
Open your web browser and go to:
**[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 📊 Evaluation Rules & Criteria

### 1. Company Criteria (Pre-seeded)
- **TCS**: CGPA ≥ 6.0, No active backlogs.
- **Infosys**: CGPA ≥ 6.5, Technical skill in Java OR Python.
- **Accenture**: CGPA ≥ 7.0, Minimum 1 project.
- **Wipro**: CGPA ≥ 6.0, No active backlogs.
- **Capgemini**: CGPA ≥ 6.5, Technical skill in SQL.
- **Cognizant**: CGPA ≥ 6.5, Minimum 1 project.

### 2. Employability Scoring (Max 100)
- **Academics (35 pts)**: `CGPA * 3.5` (Capped at 35)
- **Skills (35 pts)**: Data Structures (8 pts), Python (5 pts), Java (5 pts), SQL (5 pts), C++ (4 pts), HTML/CSS (3 pts), JavaScript (3 pts), Machine Learning (2 pts)
- **Projects (15 pts)**: 1 Project = 5 pts, 2 Projects = 10 pts, 3+ Projects = 15 pts
- **Internships (15 pts)**: Yes = 15 pts, No = 0 pts

Project updated by Sanjana Gupta.

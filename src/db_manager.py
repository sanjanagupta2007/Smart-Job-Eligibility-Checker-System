import os
import pandas as pd

# Define paths relative to the file location
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "database")
COMPANIES_CSV = os.path.join(DB_DIR, "companies.csv")
STUDENTS_CSV = os.path.join(DB_DIR, "students.csv")

def load_companies():
    """
    Loads company criteria from database/companies.csv.
    If the file does not exist, returns a default DataFrame with standard criteria.
    """
    if not os.path.exists(COMPANIES_CSV):
        # Setup folder if not exists
        os.makedirs(DB_DIR, exist_ok=True)
        # Create default CSV content
        default_data = [
            {"Company": "TCS", "MinCGPA": 6.0, "MaxBacklogs": 0, "MinProjects": 0, "RequiredSkills": None, "SkillsOperator": None},
            {"Company": "Infosys", "MinCGPA": 6.5, "MaxBacklogs": -1, "MinProjects": 0, "RequiredSkills": "Java,Python", "SkillsOperator": "OR"},
            {"Company": "Accenture", "MinCGPA": 7.0, "MaxBacklogs": -1, "MinProjects": 1, "RequiredSkills": None, "SkillsOperator": None},
            {"Company": "Wipro", "MinCGPA": 6.0, "MaxBacklogs": 0, "MinProjects": 0, "RequiredSkills": None, "SkillsOperator": None},
            {"Company": "Capgemini", "MinCGPA": 6.5, "MaxBacklogs": -1, "MinProjects": 0, "RequiredSkills": "SQL", "SkillsOperator": "AND"},
            {"Company": "Cognizant", "MinCGPA": 6.5, "MaxBacklogs": -1, "MinProjects": 1, "RequiredSkills": None, "SkillsOperator": None}
        ]
        df = pd.DataFrame(default_data)
        df.to_csv(COMPANIES_CSV, index=False)
        return df
    
    # Read and clean NaN values for clean processing
    df = pd.read_csv(COMPANIES_CSV)
    df = df.fillna("")
    return df

def load_students():
    """
    Loads all student profiles from database/students.csv.
    """
    if not os.path.exists(STUDENTS_CSV):
        os.makedirs(DB_DIR, exist_ok=True)
        cols = [
            "Name", "Branch", "GraduationYear", "TenPercent", "TwelvePercent", 
            "CGPA", "ActiveBacklogs", "Skills", "Projects", "Internship", 
            "EmployabilityScore", "ReadinessPercentage"
        ]
        df = pd.DataFrame(columns=cols)
        df.to_csv(STUDENTS_CSV, index=False)
        return df
    
    df = pd.read_csv(STUDENTS_CSV)
    # Replace NaN skills with empty string
    if "Skills" in df.columns:
        df["Skills"] = df["Skills"].fillna("")
    return df

def save_student(student_data):
    """
    Saves a student record to students.csv. If name matches an existing student, 
    overwrites their record to prevent duplicates.
    """
    os.makedirs(DB_DIR, exist_ok=True)
    df = load_students()
    
    # Format Skills if passed as list/set
    if isinstance(student_data.get("Skills"), (list, set)):
        student_data["Skills"] = ",".join(student_data["Skills"])
        
    new_row = pd.DataFrame([student_data])
    
    # De-duplicate by Name
    if not df.empty and "Name" in df.columns:
        df = df[df["Name"].str.lower() != str(student_data["Name"]).lower()]
        
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(STUDENTS_CSV, index=False)
    return True

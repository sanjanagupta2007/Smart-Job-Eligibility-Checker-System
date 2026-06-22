import os
from flask import Flask, render_template, jsonify, request
import pandas as pd

from src import db_manager
from src import analyzer
from src import charts
from src import report

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    """Renders the main dashboard page."""
    return render_template('index.html')

@app.route('/api/companies', methods=['GET'])
def get_companies():
    """Returns the list of companies and their criteria in JSON format."""
    try:
        df = db_manager.load_companies()
        # Convert NaN/None columns to empty values for cleaner JSON
        records = df.to_dict(orient='records')
        return jsonify(records)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/students', methods=['GET'])
def get_students():
    """Returns the history of saved student profiles in JSON format."""
    try:
        df = db_manager.load_students()
        records = df.to_dict(orient='records')
        return jsonify(records)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/students', methods=['POST'])
def add_student():
    """Appends or updates a student profile in the database."""
    try:
        data = request.json
        if not data or not data.get("Name"):
            return jsonify({"error": "Invalid student data. 'Name' is required."}), 400
        
        # Save record
        db_manager.save_student(data)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/check', methods=['POST'])
def check_placement_eligibility():
    """
    Accepts student details, calculates placement eligibility, score, recommendations,
    cohort analysis, and generates base64-encoded chart images.
    """
    try:
        student_profile = request.json
        if not student_profile or not student_profile.get("Name"):
            return jsonify({"error": "Invalid student profile. Name is required."}), 400
        
        # 1. Load companies criteria and existing students directory
        companies_df = db_manager.load_companies()
        students_df = db_manager.load_students()
        
        # 2. Perform score & eligibility calculations
        score_results = analyzer.calculate_employability_score(student_profile)
        eligible, ineligible = analyzer.check_eligibility(student_profile, companies_df)
        skill_gaps = analyzer.analyze_skill_gap(student_profile, companies_df)
        recs = analyzer.get_recommendations(student_profile, (eligible, ineligible))
        
        # 3. Generate placement text report
        txt_report = report.generate_text_report(
            student_profile, 
            score_results, 
            (eligible, ineligible), 
            skill_gaps, 
            recs
        )
        
        # 4. Generate base64 Matplotlib charts
        chart_eligibility_b64 = charts.generate_eligibility_chart(len(eligible), len(ineligible))
        chart_score_b64 = charts.generate_score_breakdown_chart(score_results["breakdown"])
        
        # Get student's skills list
        skills = student_profile.get("Skills", [])
        if isinstance(skills, str):
            skills = [s.strip() for s in skills.split(",") if s.strip()]
            
        chart_peers_b64 = charts.generate_peer_skills_chart(skills, students_df)
        
        # Return response bundle
        return jsonify({
            "student": student_profile,
            "score": score_results,
            "eligible": eligible,
            "ineligible": ineligible,
            "skill_gaps": skill_gaps,
            "recommendations": recs,
            "report": txt_report,
            "charts": {
                "eligibility": chart_eligibility_b64,
                "score": chart_score_b64,
                "peers": chart_peers_b64
            }
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Setup database file templates if not already present
    db_manager.load_companies()
    db_manager.load_students()
    
    print("Starting Placement Checker Server on http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

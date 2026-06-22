def calculate_employability_score(student_profile):
    """
    Calculates the employability score out of 100 based on:
    - CGPA: max 35 points (CGPA * 3.5)
    - Skills: max 35 points (weighted distribution)
    - Projects: max 15 points (1 project = 5 pts, 2 = 10 pts, 3+ = 15 pts)
    - Internship: max 15 points (Yes = 15 pts, No = 0 pts)
    """
    # 1. CGPA Score (Max 35)
    cgpa = float(student_profile.get("CGPA", 0))
    cgpa_score = min(cgpa * 3.5, 35.0)

    # 2. Skills Score (Max 35)
    skills = student_profile.get("Skills", [])
    if isinstance(skills, str):
        skills = [s.strip() for s in skills.split(",") if s.strip()]
    
    # Normalize skill names
    skills_normalized = {s.lower().replace(" ", "").replace("/", "") for s in skills}
    
    # Weights for skills: Sum = 8 + 5 + 5 + 5 + 4 + 3 + 3 + 2 = 35
    skill_weights = {
        "datastructures": 8,
        "python": 5,
        "java": 5,
        "sql": 5,
        "c++": 4,
        "htmlcss": 3,
        "javascript": 3,
        "machinelearning": 2
    }
    
    skills_score = 0.0
    for skill_key, weight in skill_weights.items():
        if skill_key in skills_normalized:
            skills_score += weight
        # Special mappings
        elif skill_key == "htmlcss" and ("html" in skills_normalized or "css" in skills_normalized):
            skills_score += weight
        elif skill_key == "c++" and ("cpp" in skills_normalized or "cplusplus" in skills_normalized):
            skills_score += weight

    # 3. Projects Score (Max 15)
    projects = int(student_profile.get("Projects", 0))
    if projects == 1:
        projects_score = 5.0
    elif projects == 2:
        projects_score = 10.0
    elif projects >= 3:
        projects_score = 15.0
    else:
        projects_score = 0.0

    # 4. Internship Score (Max 15)
    internship = student_profile.get("Internship", "No")
    internship_score = 15.0 if internship == "Yes" else 0.0

    total_score = cgpa_score + skills_score + projects_score + internship_score
    
    # Round to 1 decimal place
    return {
        "total": round(total_score, 1),
        "breakdown": {
            "academics": round(cgpa_score, 1),
            "skills": round(skills_score, 1),
            "projects": round(projects_score, 1),
            "internship": round(internship_score, 1)
        }
    }

def check_eligibility(student_profile, companies_df):
    """
    Checks the student's eligibility against all companies.
    Returns:
      - eligible: list of dicts with company details
      - ineligible: list of dicts with company details + rejection_reasons
    """
    eligible = []
    ineligible = []
    
    cgpa = float(student_profile.get("CGPA", 0.0))
    has_backlogs = student_profile.get("ActiveBacklogs", "No") == "Yes"
    projects = int(student_profile.get("Projects", 0))
    
    student_skills = student_profile.get("Skills", [])
    if isinstance(student_skills, str):
        student_skills = [s.strip() for s in student_skills.split(",") if s.strip()]
    student_skills_lower = [s.lower().strip() for s in student_skills]

    for _, row in companies_df.iterrows():
        comp_name = row["Company"]
        min_cgpa = float(row["MinCGPA"])
        max_backlogs = int(row["MaxBacklogs"])
        min_projects = int(row["MinProjects"])
        req_skills_str = row["RequiredSkills"]
        skills_op = row["SkillsOperator"]
        
        reasons = []
        
        # 1. CGPA check
        if cgpa < min_cgpa:
            reasons.append(f"CGPA is {cgpa:.2f} (Minimum required: {min_cgpa:.2f})")
            
        # 2. Backlogs check
        if max_backlogs == 0 and has_backlogs:
            reasons.append("Active backlogs are not allowed")
            
        # 3. Projects check
        if projects < min_projects:
            reasons.append(f"Projects count is {projects} (Minimum required: {min_projects})")
            
        # 4. Skills check
        req_skills = []
        if req_skills_str and isinstance(req_skills_str, str):
            req_skills = [s.strip() for s in req_skills_str.split(",") if s.strip()]
            
        if req_skills:
            has_matching_skill = False
            missing_skills = []
            
            for req_skill in req_skills:
                # Basic normalization for check
                req_normalized = req_skill.lower().replace(" ", "").replace("/", "")
                match_found = False
                for sk in student_skills_lower:
                    sk_normalized = sk.replace(" ", "").replace("/", "")
                    if req_normalized in sk_normalized or sk_normalized in req_normalized:
                        match_found = True
                        break
                
                if match_found:
                    has_matching_skill = True
                else:
                    missing_skills.append(req_skill)
            
            if skills_op == "OR":
                if not has_matching_skill:
                    reasons.append(f"Requires at least one of these skills: {', '.join(req_skills)}")
            elif skills_op == "AND":
                if missing_skills:
                    reasons.append(f"Missing required skills: {', '.join(missing_skills)}")
                    
        # Classify company
        company_status = {
            "Company": comp_name,
            "MinCGPA": min_cgpa,
            "MaxBacklogs": "No Backlogs" if max_backlogs == 0 else "Allowed",
            "MinProjects": min_projects,
            "RequiredSkills": req_skills_str if req_skills_str else "None",
            "SkillsOperator": skills_op if skills_op else "N/A"
        }
        
        if reasons:
            company_status["Reasons"] = reasons
            ineligible.append(company_status)
        else:
            eligible.append(company_status)
            
    return eligible, ineligible

def analyze_skill_gap(student_profile, companies_df):
    """
    Identifies the skill gaps for the student across all companies.
    """
    student_skills = student_profile.get("Skills", [])
    if isinstance(student_skills, str):
        student_skills = [s.strip() for s in student_skills.split(",") if s.strip()]
    student_skills_lower = [s.lower().strip() for s in student_skills]
    
    gaps = {}
    for _, row in companies_df.iterrows():
        comp_name = row["Company"]
        req_skills_str = row["RequiredSkills"]
        skills_op = row["SkillsOperator"]
        
        if not req_skills_str or not isinstance(req_skills_str, str):
            continue
            
        req_skills = [s.strip() for s in req_skills_str.split(",") if s.strip()]
        missing_skills = []
        
        for req_skill in req_skills:
            req_normalized = req_skill.lower().replace(" ", "").replace("/", "")
            match_found = False
            for sk in student_skills_lower:
                sk_normalized = sk.replace(" ", "").replace("/", "")
                if req_normalized in sk_normalized or sk_normalized in req_normalized:
                    match_found = True
                    break
            if not match_found:
                missing_skills.append(req_skill)
                
        # If it's OR and student has at least one, there is no gap.
        if skills_op == "OR":
            has_any = len(missing_skills) < len(req_skills)
            if not has_any:
                gaps[comp_name] = f"Any of: {', '.join(req_skills)}"
        elif skills_op == "AND" and missing_skills:
            gaps[comp_name] = ", ".join(missing_skills)
            
    return gaps

def get_recommendations(student_profile, eligibility_results):
    """
    Generates personalized recommendations based on the eligibility check.
    """
    eligible, ineligible = eligibility_results
    cgpa = float(student_profile.get("CGPA", 0.0))
    has_backlogs = student_profile.get("ActiveBacklogs", "No") == "Yes"
    projects = int(student_profile.get("Projects", 0))
    internship = student_profile.get("Internship", "No")
    
    student_skills = student_profile.get("Skills", [])
    if isinstance(student_skills, str):
        student_skills = [s.strip() for s in student_skills.split(",") if s.strip()]
    student_skills_lower = [s.lower().strip() for s in student_skills]
    
    skills_to_learn = []
    certifications = []
    improvements = []
    
    # 1. CGPA recommendations
    if cgpa < 7.0:
        target_diff = 7.0 - cgpa
        improvements.append(f"Focus on increasing your CGPA by at least {target_diff:.2f} points. Companies like Accenture require a minimum of 7.0 CGPA.")
    elif cgpa < 8.0:
        improvements.append("Maintain or push your CGPA above 8.0 to stay highly competitive for premium/dream packages.")
        
    # 2. Backlogs recommendations
    if has_backlogs:
        improvements.append("Prioritize clearing your active backlogs immediately. TCS and Wipro reject candidates with active backlogs.")
        
    # 3. Projects recommendations
    if projects == 0:
        improvements.append("Build at least 2 hands-on projects. Most companies (Accenture, Cognizant, etc.) require minimum 1 project to qualify.")
    elif projects == 1:
        improvements.append("Build 1 more project (target 2-3 total) to strengthen your resume and qualify for Accenture and Cognizant with a robust portfolio.")
        
    # 4. Internship recommendations
    if internship == "No":
        improvements.append("Apply for summer/virtual internships or industry training programs. Internships add 15 points to your employability score.")
        
    # 5. Skills analysis
    # High priority missing core skills
    core_skills = ["data structures", "python", "sql", "java"]
    for skill in core_skills:
        skill_normalized = skill.replace(" ", "")
        found = False
        for sk in student_skills_lower:
            if skill_normalized in sk.replace(" ", ""):
                found = True
                break
        if not found:
            skills_to_learn.append(skill.title())
            
    # Certifications mapping based on missing core skills
    if "data structures" not in [s.lower() for s in skills_to_learn]:
        pass # Student has it
    else:
        certifications.append("NPTEL or Coursera: Data Structures & Algorithms")
        
    if "python" in [s.lower() for s in skills_to_learn]:
        certifications.append("Coursera: Python for Everybody Specialization")
    if "java" in [s.lower() for s in skills_to_learn]:
        certifications.append("Oracle Certified Professional: Java SE Developer")
    if "sql" in [s.lower() for s in skills_to_learn]:
        certifications.append("Google Data Analytics Professional Certificate (SQL module)")
        
    # Machine learning recommendation if missing
    ml_found = any("machine" in sk or "ml" in sk for sk in student_skills_lower)
    if not ml_found:
        skills_to_learn.append("Machine Learning")
        certifications.append("Stanford / DeepLearning.AI: Machine Learning Specialization")
        
    # Clean up duplicate/empty values
    skills_to_learn = list(dict.fromkeys(skills_to_learn))
    certifications = list(dict.fromkeys(certifications))
    
    return {
        "skills_to_learn": skills_to_learn[:4], # limit to top 4
        "certifications": certifications[:3], # limit to top 3
        "improvements": improvements
    }

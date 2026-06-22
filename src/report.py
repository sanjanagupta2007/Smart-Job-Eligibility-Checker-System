import datetime

def generate_text_report(student_profile, score_results, eligibility_results, skill_gaps, recommendations):
    """
    Generates a detailed, professionally-formatted text report for campus placement readiness.
    """
    eligible, ineligible = eligibility_results
    total_companies = len(eligible) + len(ineligible)
    readiness_pct = (len(eligible) / total_companies * 100) if total_companies > 0 else 0.0
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""========================================================================
             CAMPUS PLACEMENT ELIGIBILITY & READINESS REPORT
========================================================================
Generated on: {timestamp}
Project: Smart Job Eligibility Checker System

------------------------------------------------------------------------
1. STUDENT PROFILE SUMMARY
------------------------------------------------------------------------
Full Name:          {student_profile.get("Name", "N/A")}
Branch:             {student_profile.get("Branch", "N/A")}
Graduation Year:    {student_profile.get("GraduationYear", "N/A")}
10th Percentage:    {student_profile.get("TenPercent", "0.0")}%
12th Percentage:    {student_profile.get("TwelvePercent", "0.0")}%
Current CGPA:       {student_profile.get("CGPA", "0.0")}
Active Backlogs:    {student_profile.get("ActiveBacklogs", "No")}
Skills:             {student_profile.get("Skills", "None")}
Projects Done:      {student_profile.get("Projects", "0")}
Internship Done:    {student_profile.get("Internship", "No")}

------------------------------------------------------------------------
2. PLACEMENT READINESS METRICS
------------------------------------------------------------------------
Employability Score:   {score_results.get("total", 0.0)} / 100.0
Readiness Rating:      {get_score_rating(score_results.get("total", 0.0))}

Score Breakdown:
  - Academic Performance:  {score_results["breakdown"].get("academics", 0.0)} / 35.0
  - Technical Skill Set:   {score_results["breakdown"].get("skills", 0.0)} / 35.0
  - Project Work:          {score_results["breakdown"].get("projects", 0.0)} / 15.0
  - Internship Experience: {score_results["breakdown"].get("internship", 0.0)} / 15.0

Company Eligibility:
  - Eligible Companies:    {len(eligible)} / {total_companies}
  - Target Eligibility:    {readiness_pct:.1f}%

------------------------------------------------------------------------
3. COMPANY ELIGIBILITY STATUS
------------------------------------------------------------------------
"""

    if eligible:
        report += "ELIGIBLE FOR:\n"
        for comp in eligible:
            report += f"  [✔] {comp['Company']}\n"
            report += f"      Criteria met: CGPA >= {comp['MinCGPA']} | Projects >= {comp['MinProjects']}\n"
    else:
        report += "ELIGIBLE FOR:\n  [!] None of the listed companies.\n"
        
    report += "\n"
    
    if ineligible:
        report += "INELIGIBLE FOR:\n"
        for comp in ineligible:
            report += f"  [✘] {comp['Company']}\n"
            report += f"      Rejection Reasons:\n"
            for reason in comp['Reasons']:
                report += f"        - {reason}\n"
    else:
        report += "INELIGIBLE FOR:\n  [✔] None (Eligible for all companies!)\n"
        
    report += """
------------------------------------------------------------------------
4. SKILL GAP ANALYSIS
------------------------------------------------------------------------
"""
    if skill_gaps:
        for company, gap in skill_gaps.items():
            report += f"  * {company}: Missing [{gap}]\n"
    else:
        report += "  [✔] No technical skill gaps detected for the target companies.\n"
        
    report += """
------------------------------------------------------------------------
5. PERSONALIZED RECOMMENDATIONS & ACTION PLAN
------------------------------------------------------------------------
"""
    # Action items/improvements
    if recommendations.get("improvements"):
        report += "Action Items to Improve Eligibility:\n"
        for idx, imp in enumerate(recommendations["improvements"], 1):
            report += f"  {idx}. {imp}\n"
        report += "\n"
    else:
        report += "Action Items to Improve Eligibility:\n  [✔] You already meet all base requirements! Keep maintaining your records.\n\n"
        
    # Skills to learn
    if recommendations.get("skills_to_learn"):
        report += "Skills to Acquire:\n"
        for skill in recommendations["skills_to_learn"]:
            report += f"  - {skill}\n"
        report += "\n"
        
    # Suggested Certifications
    if recommendations.get("certifications"):
        report += "Suggested Professional Certifications:\n"
        for cert in recommendations["certifications"]:
            report += f"  - {cert}\n"
    
    report += """
========================================================================
                         END OF REPORT
========================================================================
"""
    return report

def get_score_rating(score):
    if score >= 85:
        return "Excellent Readiness (Highly Placement Ready)"
    elif score >= 70:
        return "Good Readiness (Placement Ready, minor gaps)"
    elif score >= 50:
        return "Average Readiness (Needs improvements in projects/skills)"
    else:
        return "Needs Attention (High priority improvements required)"

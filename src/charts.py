import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def fig_to_base64(fig):
    """
    Saves a Matplotlib figure to a bytes buffer and encodes it as a base64 string.
    Closes the figure to free up memory.
    """
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=100, transparent=True)
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return img_str

def generate_eligibility_chart(eligible_count, ineligible_count):
    """
    Generates a donut chart showing eligible vs ineligible companies.
    """
    labels = ['Eligible', 'Ineligible']
    sizes = [eligible_count, ineligible_count]
    colors = ['#10b981', '#ef4444'] # Emerald Green, Rose Red
    
    # Handle edge case where both are zero
    if eligible_count == 0 and ineligible_count == 0:
        sizes = [1, 0]
        labels = ['No Data', '']
        colors = ['#9ca3af', '#e5e7eb']

    fig, ax = plt.subplots(figsize=(4.5, 4.5))
    
    # Create pie chart
    wedges, texts, autotexts = ax.pie(
        sizes, 
        labels=labels, 
        colors=colors, 
        autopct='%1.0f%%', 
        startangle=90,
        pctdistance=0.75,
        textprops=dict(color="#1f2937", weight="bold")
    )
    
    # Draw center circle to turn it into a donut
    centre_circle = plt.Circle((0,0), 0.55, fc='white')
    fig.gca().add_artist(centre_circle)
    
    # Customize layout
    ax.axis('equal')  
    plt.tight_layout()
    
    # Style text labels
    for text in texts:
        text.set_color('#374151')
        text.set_fontsize(10)
    for autotext in autotexts:
        autotext.set_color('#ffffff')
        autotext.set_fontsize(11)

    return fig_to_base64(fig)

def generate_score_breakdown_chart(score_breakdown):
    """
    Generates a horizontal bar chart of the student's employability score categories 
    compared to the maximum points for each.
    """
    categories = ['Internship\n(Max 15)', 'Projects\n(Max 15)', 'Skills\n(Max 35)', 'Academics\n(Max 35)']
    scores = [
        score_breakdown.get('internship', 0),
        score_breakdown.get('projects', 0),
        score_breakdown.get('skills', 0),
        score_breakdown.get('academics', 0)
    ]
    max_scores = [15, 15, 35, 35]
    
    y_pos = np.arange(len(categories))
    
    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    
    # Plot backgrounds (max scores) in light grey
    ax.barh(y_pos, max_scores, color='#e5e7eb', height=0.5, label='Max Score')
    # Plot student scores in premium Indigo/Teal
    bars = ax.barh(y_pos, scores, color='#6366f1', height=0.5, label='Your Score')
    
    # Customize labels and borders
    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories, fontsize=9, color='#374151', fontweight='semibold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_color('#d1d5db')
    ax.xaxis.set_visible(False)
    
    # Add labels showing scores on top of bars
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + 0.5, 
            bar.get_y() + bar.get_height()/2, 
            f'{width:.1f}', 
            ha='left', 
            va='center', 
            fontsize=9, 
            color='#1f2937', 
            fontweight='bold'
        )
        
    plt.tight_layout()
    return fig_to_base64(fig)

def generate_peer_skills_chart(student_skills, students_df):
    """
    Generates a chart showing the frequency of core skills among peers (from student database)
    and highlights whether the current student possesses each skill.
    """
    core_skills = ["Data Structures", "Python", "SQL", "Java", "C++", "HTML/CSS", "JavaScript", "Machine Learning"]
    
    # Normalize student's skills
    if isinstance(student_skills, str):
        student_skills = [s.strip() for s in student_skills.split(",") if s.strip()]
    student_skills_lower = [s.lower().strip() for s in student_skills]
    
    # Default peer frequencies if there are too few entries in the database
    default_frequencies = {
        "Data Structures": 0.75,
        "Python": 0.65,
        "SQL": 0.60,
        "Java": 0.50,
        "C++": 0.45,
        "HTML/CSS": 0.55,
        "JavaScript": 0.50,
        "Machine Learning": 0.30
    }
    
    frequencies = {}
    total_students = len(students_df)
    
    if total_students >= 2:
        # Calculate actual frequencies from database
        for skill in core_skills:
            count = 0
            skill_normalized = skill.lower().replace(" ", "").replace("/", "")
            for _, student in students_df.iterrows():
                std_skills = str(student.get("Skills", "")).lower().replace(" ", "").replace("/", "")
                if skill_normalized in std_skills:
                    count += 1
            frequencies[skill] = count / total_students
    else:
        frequencies = default_frequencies

    # Sort skills by peer frequency
    sorted_skills = sorted(core_skills, key=lambda x: frequencies[x], reverse=True)
    sorted_freqs = [frequencies[s] * 100 for s in sorted_skills]
    
    # Determine bar colors: teal/indigo if the student has it, grey if not
    colors = []
    for skill in sorted_skills:
        skill_normalized = skill.lower().replace(" ", "").replace("/", "")
        has_skill = False
        for sk in student_skills_lower:
            sk_normalized = sk.replace(" ", "").replace("/", "")
            if skill_normalized in sk_normalized or sk_normalized in skill_normalized:
                has_skill = True
                break
        colors.append('#0d9488' if has_skill else '#cbd5e1') # Teal if student has, Light Slate Grey if missing

    fig, ax = plt.subplots(figsize=(6.5, 3.5))
    x_pos = np.arange(len(sorted_skills))
    
    # Plot vertical bars
    bars = ax.bar(x_pos, sorted_freqs, color=colors, width=0.55)
    
    # Styling labels and axes
    ax.set_xticks(x_pos)
    ax.set_xticklabels(sorted_skills, rotation=35, ha='right', fontsize=8, color='#374151', fontweight='semibold')
    ax.set_ylabel('Peer Possession Rate (%)', fontsize=9, color='#4b5563', fontweight='bold')
    ax.set_ylim(0, 110)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#d1d5db')
    ax.spines['bottom'].set_color('#d1d5db')
    
    # Add % labels on top of the bars
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2., 
            height + 2, 
            f'{height:.0f}%', 
            ha='center', 
            va='bottom', 
            fontsize=8, 
            color='#4b5563', 
            fontweight='bold'
        )
        
    # Legend info in title or labels
    ax.set_title('Skill Comparison (Green = You Have, Grey = Missing)', fontsize=10, pad=15, color='#1f2937', fontweight='bold')
    
    plt.tight_layout()
    return fig_to_base64(fig)

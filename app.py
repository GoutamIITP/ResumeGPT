from flask import Flask, request, render_template
from transformers import pipeline
import uuid

app = Flask(__name__)

# Load the resume template
with open("resume_template.txt", "r") as file:
    resume_template = file.read()

# Initialize the generative AI model (Hugging Face BART for demo)
generator = pipeline("text2text-generation", model="facebook/bart-large")

def generate_resume_content(job_description, eligibility, skills, name, email, phone):
    # Create a prompt for the AI model
    prompt = f"""
    Given the following job description, eligibility criteria, and skills, generate content for a resume tailored to the job role.
    Job Description: {job_description}
    Eligibility Criteria: {eligibility}
    Skills: {skills}
    Provide content for the following sections:
    - Objective: A concise statement tailored to the job role.
    - Skills: 4 bullet points based on the provided skills and job requirements.
    - Professional Experience: 2 jobs with 2 responsibilities and 1 achievement each, aligned with the job description and eligibility.
    - Education: 1 degree with relevant coursework or honors.
    - Certifications: 2 relevant certifications.
    Return the content with placeholders like [AI-generated objective], [AI-generated skill 1], etc., matching the resume template.
    """
    
    # Generate content using the AI model
    try:
        generated = generator(prompt, max_length=600, num_return_sequences=1)[0]["generated_text"]
    except Exception as e:
        generated = "Error generating content. Please try again."

    # For demo purposes, parse the generated content with fallback placeholders
    # In production, parse the AI output more robustly (e.g., regex or JSON)
    placeholders = {
        "[Full Name]": name,
        "[Email Address]": email,
        "[Phone Number]": phone,
        "[LinkedIn/Portfolio]": "linkedin.com/in/" + name.replace(" ", "").lower(),
        "[AI-generated objective]": f"To secure a position as a {job_description.split(' at ')[0]} where I can utilize my expertise in {skills.split(', ')[0]} and {skills.split(', ')[1]} to contribute to organizational goals." if ', ' in skills else generated, # Use generated as fallback
        "[AI-generated skill 1]": skills.split(', ')[0] if ', ' in skills else "Skill 1",
        "[AI-generated skill 2]": skills.split(', ')[1] if len(skills.split(', ')) > 1 else "Team Collaboration",
        "[AI-generated skill 3]": skills.split(', ')[2] if len(skills.split(', ')) > 2 else "Problem Solving",
        "[AI-generated skill 4]": skills.split(', ')[3] if len(skills.split(', ')) > 3 else "Project Management",
        "[AI-generated job title 1]": job_description.split(' at ')[0] if ' at ' in job_description else "Job Title 1",
        "[Company Name]": job_description.split(' at ')[1] if ' at ' in job_description else "Tech Corp",
        "[Dates]": "Jan 2022 - Present",
        "[AI-generated responsibility 1]": f"Developed solutions using {skills.split(', ')[0]}." if ', ' in skills else "Responsibility 1",
        "[AI-generated responsibility 2]": f"Collaborated with teams to meet {eligibility.split(', ')[0].lower()} requirements." if ', ' in eligibility else "Responsibility 2",
        "[AI-generated achievement 1]": f"Improved process efficiency by 15% through {skills.split(', ')[1] if len(skills.split(', ')) > 1 else 'optimization'}." if ', ' in skills else "Achievement 1",
        "[AI-generated job title 2]": "Junior " + job_description.split(' at ')[0] if ' at ' in job_description else "Job Title 2",
        "[AI-generated responsibility 1]": f"Supported development of {skills.split(', ')[0]}-based projects." if ', ' in skills else "Responsibility 1",
        "[AI-generated responsibility 2]": "Assisted in implementing best practices.",
        "[AI-generated achievement 1]": f"Reduced project delivery time by 10% using {skills.split(', ')[1] if len(skills.split(', ')) > 1 else 'streamlined workflows'}." if ', ' in skills else "Achievement 1",
        "[AI-generated degree]": eligibility.split(', ')[0] if 'degree' in eligibility.lower() else "B.S. in Computer Science",
        "[University Name]": "State University",
        "[Year]": "2021",
        "[AI-generated relevant coursework or honors]": "Relevant Coursework: " + ", ".join(skills.split(', ')[:2]) if ', ' in skills else "Coursework/Honors",
        "[AI-generated certification 1]": f"Certified {skills.split(', ')[0]} Professional" if ', ' in skills else "Certification 1",
        "[AI-generated certification 2]": f"Advanced {skills.split(', ')[1] if len(skills.split(', ')) > 1 else 'Technical'} Certification" if ', ' in skills else "Certification 2"
    }
    
    # Replace placeholders in the template
    resume_content = resume_template
    for placeholder, value in placeholders.items():
        resume_content = resume_content.replace(placeholder, str(value))
    
    return resume_content

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        job_description = request.form["job_description"]
        eligibility = request.form["eligibility"]
        skills = request.form["skills"]
        
        # Generate resume content
        resume_content = generate_resume_content(job_description, eligibility, skills, name, email, phone)
        return render_template("resume.html", resume_content=resume_content)
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True) 
ResumeGPT

ResumeGPT is a Gen AI-powered job application system that parses resumes, matches them to job descriptions, creates ATS-friendly resumes, submits applications, and schedules interviews.

Setup

```bash
Clone the repository:

git clone https://github.com/yourusername/resumegpt.git
cd resumegpt
```

```bash
Create a virtual environment and install dependencies:

python -m venv resumegpt_env
source resumegpt_env/bin/activate
pip install -r requirements.txt
```

(Optional) Set up Gen AI:

* For Hugging Face: Ensure torch is installed.

* For xAI Grok 3 API: Obtain a key from https://x.ai/api.

```bash
Run the application:

python app.py
```

Usage

* Visit http://localhost:5000.

* Upload a resume (PDF/Word) and specify job preferences (e.g., role, location).

* The system parses the resume, matches jobs, generates ATS-friendly resumes, submits applications, and schedules interviews.

* View results on the results page.

Ethical Guidelines

* Respect job board terms of service and robots.txt.

* Limit submissions to avoid spamming.

* User data is encrypted and complies with GDPR/CCPA.

* Obtain user consent for automated actions.

Dependencies

* Flask

* PyPDF2

* pdfplumber

* transformers

* torch

* requests

* BeautifulSoup

* Selenium

* Pandas

* reportlab 
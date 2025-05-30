# ResumeGPT

## Project Overview

ResumeGPT is a web application built with Flask and a generative AI model (initially using Hugging Face, with planned integration for xAI's Grok API) that helps users create tailored resumes based on a job description, eligibility criteria, and their skills.

Users provide their personal details, the job description, eligibility requirements, and a list of their skills through a simple web form. The application then uses the AI model to generate relevant content for different sections of a resume, such as the objective, skills, experience, education, and certifications. Finally, it presents the generated resume content in a structured format, which can also be downloaded as a text file.

## Features

*   **Tailored Resume Generation:** Generates resume content based on user inputs (job description, eligibility, skills).
*   **Personal Information Integration:** Incorporates user's name, email, phone number, and LinkedIn/portfolio link into the resume.
*   **Web Interface:** Provides a simple and intuitive web form for input and displays the generated resume.
*   **Download Option:** Allows users to download the generated resume as a text file.
*   **Modular Design:** Uses a resume template for easy structure modification.
*   **Virtual Environment:** Project set up within a Python virtual environment for dependency management.

## Setup and Installation

Follow these steps to set up and run the ResumeGPT application locally:

1.  **Clone the repository (if applicable) or navigate to the project directory:**

    ```bash
    cd /path/to/your/ResumeGPT
    ```

2.  **Create a Python Virtual Environment:**

    It's recommended to use a virtual environment to manage dependencies.

    ```bash
    python -m venv .venv
    ```

3.  **Activate the Virtual Environment:**

    *   **On Windows:**

        ```bash
        .venv\Scripts\Activate.ps1
        ```

    *   **On macOS and Linux:**

        ```bash
        source .venv/bin/activate
        ```

4.  **Install Dependencies:**

    Install the required Python packages using pip:

    ```bash
    pip install flask transformers requests
    ```

## Project Structure

The project directory has the following structure:

```
ResumeGPT/
├── app.py                # Main Flask application file
├── templates/
│   ├── index.html        # Input form HTML template
│   └── resume.html       # Generated resume output HTML template
├── static/
│   └── style.css         # CSS file for styling
├── resume_template.txt   # Template for structuring the resume content
└── .venv/                # Python virtual environment (generated after setup)
```

## How to Run the Application

1.  **Activate the virtual environment** (if not already active):

    *   **On Windows:** `.venv\Scripts\Activate.ps1`
    *   **On macOS and Linux:** `source .venv/bin/activate`

2.  **Run the Flask application:**

    ```bash
    python app.py
    ```

3.  **Access the application:**

    Open your web browser and go to `http://127.0.0.1:5000`.

## AI Model Usage

The application currently uses the `facebook/bart-large` model from Hugging Face for generating resume content as a demonstration. This model may not produce highly accurate or tailored results for all job descriptions and eligibility criteria.

**Using xAI's Grok API (for Production):**

For better results in a production environment, it is recommended to use a more powerful model like xAI's Grok API. To integrate the Grok API:

1.  Sign up for the xAI API at [https://x.ai/api](https://x.ai/api) to obtain an API key.
2.  Update the `generate_resume_content` function in `app.py` to make API calls to the xAI Grok endpoint, including your API key in the request headers.
3.  Adjust the parsing logic in `generate_resume_content` to correctly extract the generated content from the xAI API's response format.

## Potential Enhancements

*   **Improved AI Parsing:** Implement more robust parsing of the AI model's output (using regex, JSON parsing, etc.) to accurately populate the resume template sections.
*   **LaTeX Output:** Add functionality to generate the resume in LaTeX format for creating professional PDF documents.
*   **Advanced UI:** Enhance the user interface using frameworks like Tailwind CSS or Bootstrap.
*   **Error Handling and Input Validation:** Implement more comprehensive error handling and validate user inputs.
*   **Database Integration:** Store user inputs and generated resumes in a database.
*   **Advanced AI Integration:** Explore using features like xAI's DeepSearch (if available) for more context-aware resume generation.

## License

[Specify your project's license here, e.g., MIT, Apache 2.0, etc.] 
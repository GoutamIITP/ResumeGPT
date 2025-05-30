import requests

def schedule_interview(email, calendly_link):
    # Send Calendly link to employer (mock implementation)
    payload = {
        "email": email,
        "calendly_link": calendly_link,
        "message": "Please schedule an interview using this link."
    }
    # Replace with actual API call to email service or Calendly
    response = requests.post("https://api.example.com/send_email", json=payload)
    return response.status_code == 200

if __name__ == "__main__":
    success = schedule_interview("employer@company.com", "https://calendly.com/user/interview")
    print("Interview scheduled" if success else "Scheduling failed") 
# Study Planner Backend
This is the backend to my CMU 15-113 HW4 assignment, which is Study Session Generator.

My backend has been written in Python using Flask. It receives the input from the frontend, verifies the input and then generates the study session schedule.

## What the Backend Does
The frontend provides the following data:

- The subject
- Available study time in minutes
- Level of difficulty
- Energy level

The backend creates a structured plan for studying based on the provided data:

- Review time
- Studying/learning periods
- Breaks (if necessary)
- Final review time

The output of the algorithm is presented to the frontend in the form of JSON and displayed on the web page.

## Endpoints

### GET `/`

This endpoint checks whether the backend is running.

Example response:

```json
{
  "message": "Study Session Generator is running!",
  "endpoint": "POST /generate-plan"
}

AI USAGE: I used Codex AI with my ChatGPT Plus account in vs code and also chatgpt in the browser itself. 

Environment Variables and Secrets
Currently, this project is not using any API keys, passwords, or other secrets.
The .gitignore file ensures that the .env files and local virtual environment directories do not get uploaded to GitHub.
Any future addition of secrets in this project should be in the form of environment variables and must not be hardcoded into the program.

POST /generate-plan
Accepts study preferences and creates a study plan.
Example request:
{
  "subject": "Calculus",
  "minutes": 90,
  "difficulty": "hard",
  "energy": "medium"
}
Parameters:
- subject: non-empty subject name
- minutes: whole number between 15 and 180
- difficulty: easy, medium, or hard
- energy: low, medium, or high

How the Frontend Communicates With the Backend
The front-end sends the post request using JavaScript Fetch() to the URL /generate-plan.
This is done using JSON format. The backend receives this information and sends back the generated study plan using JSON.
The study activities received from the backend are then displayed by the frontend.
CORS is implemented through Flask-CORS. This allows the front-end and backend to run on different URLs.

The project uses:
- Flask
- Flask-Cors
- Gunicorn
These are listed in requirements.txt.
The backend is deployed on Render.
Build command:
pip install -r requirements.txt

Start command:
gunicorn app:app
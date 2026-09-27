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
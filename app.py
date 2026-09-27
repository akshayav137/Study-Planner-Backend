from flask import Flask, jsonify, request
from flask_cors import CORS


# Create the Flask application. CORS allows a separate frontend (such as
# GitHub Pages) to call these routes from a browser.
app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def home():
    """Provide a simple way to check that the backend is running."""
    return jsonify({
        "message": "Study Session Generator is running!",
        "endpoint": "POST /generate-plan",
    })


@app.route("/generate-plan", methods=["POST"])
def generate_plan():
    """Validate study preferences and create a schedule with Python rules."""
    # silent=True lets us return our own JSON error for unreadable JSON.
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({
            "error": "Send a JSON object with Content-Type: application/json."
        }), 400

    subject = data.get("subject")
    minutes = data.get("minutes")
    difficulty = data.get("difficulty")
    energy = data.get("energy")

    # Collect errors so the frontend can show all problems at once.
    errors = {}
    if not isinstance(subject, str) or not subject.strip():
        errors["subject"] = "Enter a nonempty subject name."

    # Use type(...) here because Python also treats True and False as integers.
    if type(minutes) is not int or not 15 <= minutes <= 180:
        errors["minutes"] = "Enter a whole number between 15 and 180."

    if difficulty not in ("easy", "medium", "hard"):
        errors["difficulty"] = "Choose easy, medium, or hard."

    if energy not in ("low", "medium", "high"):
        errors["energy"] = "Choose low, medium, or high."

    if errors:
        return jsonify({
            "error": "Please check your study preferences.",
            "fields": errors,
        }), 400

    subject = subject.strip()

    # Lower energy means shorter focus blocks. Hard topics also get slightly
    # shorter blocks and more time for an initial review of the basics.
    block_lengths = {"low": 15, "medium": 25, "high": 35}
    focus_minutes = block_lengths[energy]
    if difficulty == "hard":
        focus_minutes = max(10, focus_minutes - 5)

    review_percentages = {"easy": 0.10, "medium": 0.15, "hard": 0.20}
    opening_minutes = max(3, int(minutes * review_percentages[difficulty]))
    closing_minutes = max(3, min(10, minutes // 6))

    practice_instructions = {
        "easy": "Test yourself without notes, then check your answers.",
        "medium": "Practice a few problems and review any mistakes.",
        "hard": "Study a worked example, then try a similar problem yourself.",
    }

    # Every activity includes its position on a timeline starting at minute 0.
    activities = []
    elapsed = 0

    def add_activity(activity_type, title, duration, instructions):
        nonlocal elapsed
        activities.append({
            "type": activity_type,
            "title": title,
            "duration_minutes": duration,
            "start_minute": elapsed,
            "end_minute": elapsed + duration,
            "instructions": instructions,
        })
        elapsed += duration

    add_activity(
        "study", "Review and set a goal", opening_minutes,
        f"Review your {subject} notes and choose one or two concepts to practice.",
    )

    # The requested minutes include breaks. Reserve time for the final review
    # before dividing the remaining time into practice blocks and breaks.
    remaining = minutes - opening_minutes - closing_minutes
    while remaining > 0:
        duration = min(focus_minutes, remaining)
        add_activity(
            "study", f"Practice {subject}", duration,
            practice_instructions[difficulty],
        )
        remaining -= duration

        # Only add a break if at least five minutes of practice will follow.
        # A tiny leftover is folded into the current block instead.
        if remaining >= 10:
            add_activity(
                "break", "Take a break", 5,
                "Stand up, stretch, and drink some water.",
            )
            remaining -= 5
        elif remaining > 0:
            activities[-1]["duration_minutes"] += remaining
            activities[-1]["end_minute"] += remaining
            elapsed += remaining
            remaining = 0

    add_activity(
        "review", "Wrap up and recall", closing_minutes,
        f"Summarize what you learned about {subject} without looking at your "
        "notes. Write down one question to revisit next time.",
    )

    # jsonify converts Python dictionaries and lists into a JSON response.
    return jsonify({
        "subject": subject,
        "minutes": minutes,
        "difficulty": difficulty,
        "energy": energy,
        "summary": "Review, practice with breaks when time allows, then recall "
        "what you learned. Total time includes breaks.",
        "activities": activities,
    })


# This starts the local server only when you run: python app.py
if __name__ == "__main__":
    app.run()

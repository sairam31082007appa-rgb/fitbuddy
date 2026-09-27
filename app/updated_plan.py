from app.config import (
    GOOGLE_API_KEY,
    GEMINI_WORKOUT_MODEL,
)

from app.gemini_generator import demo_plan


def update_workout_plan(
    original_plan,
    feedback,
    goal,
    intensity
):

    if not GOOGLE_API_KEY:

        return (
            demo_plan(
                goal,
                intensity
            )
            +
            "\n\nUPDATE NOTE:\n"
            +
            f"The requested feedback was:\n{feedback}"
        )

    from google import genai

    client = genai.Client(
        api_key=GOOGLE_API_KEY
    )

    prompt = f"""
You are FitBuddy.

Revise the following existing 7-day workout plan
according to the user's feedback.

FITNESS GOAL:
{goal}

INTENSITY:
{intensity}

USER FEEDBACK:
{feedback}

ORIGINAL PLAN:
{original_plan}


REQUIREMENTS:

1. Return a complete revised DAY 1 through DAY 7 plan.
2. Do not return only the changed section.
3. Apply the user's feedback where practical.
4. Preserve warm-up sections.
5. Preserve cooldown/recovery sections.
6. Maintain appropriate intensity.
7. Include at least one recovery/rest-focused day.
8. Avoid medical claims.
9. Keep the output easy to read.
"""

    response = client.models.generate_content(
        model=GEMINI_WORKOUT_MODEL,
        contents=prompt
    )

    return response.text.strip()
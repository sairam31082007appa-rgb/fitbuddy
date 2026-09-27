from app.config import (
    GOOGLE_API_KEY,
    GEMINI_TIP_MODEL,
)


def generate_nutrition_tip_with_flash(goal):

    if not GOOGLE_API_KEY:
        return fallback_tip(goal)

    from google import genai

    client = genai.Client(
        api_key=GOOGLE_API_KEY
    )

    prompt = f"""
Give one concise and practical nutrition or recovery
tip for a person whose fitness goal is:

{goal}

Requirements:

- Maximum 80 words.
- Practical and easy to follow.
- Avoid medical claims.
- Avoid extreme dieting.
- Mention hydration or balanced meals when appropriate.
"""

    response = client.models.generate_content(
        model=GEMINI_TIP_MODEL,
        contents=prompt
    )

    return response.text.strip()


def fallback_tip(goal):

    tips = {

        "muscle gain":
            "Include a protein-rich food in each main meal, eat enough overall, stay hydrated, and prioritize sleep for recovery.",

        "weight loss":
            "Build meals around vegetables, a protein source, whole foods, and enough water. Focus on sustainable habits instead of extreme restriction.",

        "general wellness":
            "Aim for balanced meals containing protein, vegetables or fruit, whole grains, healthy fats, and regular hydration.",

        "flexibility":
            "Stay hydrated and combine mobility sessions with balanced meals and adequate recovery, especially after longer sessions."
    }

    return tips.get(
        goal,
        tips["general wellness"]
    )
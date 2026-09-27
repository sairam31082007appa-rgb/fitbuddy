from app.config import (
    GOOGLE_API_KEY,
    GEMINI_WORKOUT_MODEL,
)


def get_gemini_client():

    if not GOOGLE_API_KEY:
        return None

    from google import genai

    return genai.Client(
        api_key=GOOGLE_API_KEY
    )


def generate_workout_gemini(
    username,
    age,
    weight,
    goal,
    intensity
):

    client = get_gemini_client()

    prompt = f"""
You are FitBuddy, a responsible fitness planning assistant.

Create a practical personalized 7-day fitness plan.

USER INFORMATION

Name:
{username}

Age:
{age}

Weight:
{weight} kg

Fitness Goal:
{goal}

Workout Intensity:
{intensity}


OUTPUT REQUIREMENTS

Create DAY 1 through DAY 7.

For every day include:

Focus
Warm-up
Main Workout
Cooldown / Recovery

For the Main Workout include:

- Exercise name
- Sets and repetitions OR duration
- Suggested rest time


IMPORTANT RULES

1. Keep the training volume appropriate for the selected intensity.
2. Include at least one recovery/rest-focused day.
3. Keep the plan easy to understand.
4. Avoid medical diagnosis or medical treatment claims.
5. Do not recommend extreme dieting.
6. Include a short safety note at the end.
7. Use clean plain text formatting.
8. Make the plan practical for a normal user.
"""

    if client is None:
        return demo_plan(
            goal,
            intensity
        )

    response = client.models.generate_content(
        model=GEMINI_WORKOUT_MODEL,
        contents=prompt
    )

    return response.text.strip()


def demo_plan(
    goal,
    intensity
):

    return f"""
DAY 1 — FULL BODY

Focus:
{goal} foundation

Warm-up:
7 minutes brisk walking + mobility exercises.

Main Workout:
- Squats — 3 x 10
- Incline push-ups — 3 x 8
- Glute bridges — 3 x 12
- Plank — 3 x 20 seconds

Rest:
60–90 seconds between sets.

Cooldown:
5 minutes easy walking + gentle stretching.


DAY 2 — CARDIO

Focus:
Steady cardiovascular conditioning.

Warm-up:
5 minutes easy walking.

Main Workout:
25 minutes brisk walking or cycling at a comfortable
{intensity} effort.

Cooldown:
5 minutes easy walking + breathing.


DAY 3 — LOWER BODY + CORE

Focus:
Leg strength and stability.

Warm-up:
7 minutes mobility.

Main Workout:
- Reverse lunges — 3 x 8 each side
- Hip hinge — 3 x 10
- Calf raises — 3 x 15
- Dead bug — 3 x 8 each side

Cooldown:
5 minutes stretching.


DAY 4 — RECOVERY

Focus:
Active recovery.

Warm-up:
Gentle mobility.

Main Workout:
20–30 minutes easy walking.

Optional:
Light stretching.

Cooldown:
Relaxed breathing.


DAY 5 — UPPER BODY

Focus:
Upper-body strength.

Warm-up:
Shoulder circles + 5 minutes walking.

Main Workout:
- Wall/incline push-ups — 3 x 10
- Backpack rows — 3 x 10
- Shoulder raises — 2 x 12
- Bird dog — 3 x 8 each side

Cooldown:
Chest and back stretching.


DAY 6 — CARDIO + CORE

Focus:
Conditioning.

Warm-up:
5 minutes easy walking.

Main Workout:
20 minutes alternating:
1 minute faster pace
2 minutes easy pace

Then:

Plank — 3 x 20 seconds.

Cooldown:
5 minutes easy walking.


DAY 7 — REST & RESET

Focus:
Recovery.

Main Workout:
Rest.

Optional:
Relaxed walk and gentle mobility.

Recovery:
Hydration + adequate sleep.


SAFETY NOTE

Stop exercise if you experience pain, dizziness,
chest discomfort, or unusual shortness of breath,
and seek appropriate professional advice.
"""
def ask_ai_coach(
    question,
    username="FitBuddy User",
    goal="general fitness"
):

    client = get_gemini_client()

    prompt = f"""
You are FitBuddy AI Coach.

User:
{username}

Fitness Goal:
{goal}

User Question:
{question}

Give a practical, concise fitness answer.

Rules:
- Be supportive and easy to understand.
- Do not diagnose medical conditions.
- Do not prescribe medicines.
- Do not recommend extreme diets or unsafe workouts.
- If the question involves serious pain, injury, chest pain,
  dizziness, or breathing difficulty, recommend appropriate
  professional medical help.
"""

    if client is None:
        return (
            "AI Coach is currently using basic mode. "
            "Stay consistent with your workout, stay hydrated, "
            "and get enough sleep. For specific concerns, "
            "please consult a qualified professional."
        )

    response = client.models.generate_content(
        model=GEMINI_WORKOUT_MODEL,
        contents=prompt
    )

    return response.text.strip()

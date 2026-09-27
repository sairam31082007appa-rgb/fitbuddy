from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.database import (
    delete_user,
    get_all_users,
    get_user,
    save_user,
    update_plan,
)

from app.gemini_flash_generator import (
    generate_nutrition_tip_with_flash,
)

from app.gemini_generator import (
    generate_workout_gemini,
)

from app.schemas import (
    FeedbackRequest,
    UserInput,
)

from app.updated_plan import (
    update_workout_plan,
)


router = APIRouter()


# ==================================================
# TEMPLATE CONFIGURATION
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "templates"

templates = Jinja2Templates(
    directory=str(TEMPLATE_DIR)
)


# ==================================================
# HOME PAGE
# ==================================================

@router.get(
    "/",
    response_class=HTMLResponse
)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )


# ==================================================
# GENERATE WORKOUT
# ==================================================

@router.post(
    "/generate-workout",
    response_class=HTMLResponse
)
def generate_workout(
    request: Request,

    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):

    # ------------------------------------------------
    # Validate User Input
    # ------------------------------------------------

    data = UserInput(
        username=username,
        user_id=user_id,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity
    )

    # ------------------------------------------------
    # Generate Workout Plan
    # ------------------------------------------------

    workout_plan = generate_workout_gemini(
        username=data.username,
        age=data.age,
        weight=data.weight,
        goal=data.goal,
        intensity=data.intensity
    )

    # ------------------------------------------------
    # Generate Nutrition Tip
    # ------------------------------------------------

    nutrition_tip = generate_nutrition_tip_with_flash(
        data.goal
    )

    # ------------------------------------------------
    # Save User
    # ------------------------------------------------

    user = save_user({

        "user_id": data.user_id,

        "username": data.username,

        "age": data.age,

        "weight": data.weight,

        "goal": data.goal,

        "intensity": data.intensity,

        "original_plan": workout_plan,

        "nutrition_tip": nutrition_tip
    })

    # ------------------------------------------------
    # Show Result Page
    # ------------------------------------------------

    # ------------------------------------------------
    # Go to Personal Dashboard
    # ------------------------------------------------

    return RedirectResponse(
        url=f"/dashboard/{user.user_id}",
        status_code=303
    )


# ==================================================
# SUBMIT FEEDBACK
# ==================================================

@router.post(
    "/submit-feedback",
    response_class=HTMLResponse
)
def submit_feedback(
    request: Request,

    user_id: str = Form(...),

    feedback: str = Form(...)
):

    # ------------------------------------------------
    # Validate Feedback
    # ------------------------------------------------

    request_data = FeedbackRequest(
        user_id=user_id,
        feedback=feedback
    )

    # ------------------------------------------------
    # Find User
    # ------------------------------------------------

    user = get_user(
        request_data.user_id
    )

    # ------------------------------------------------
    # User Not Found
    # ------------------------------------------------

    if not user:

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "request": request,
                "user": None,
                "plan": None,
                "tip": None,
                "updated": False,
                "error": (
                    "User ID not found. "
                    "Please generate a plan first."
                )
            }
        )

    # ------------------------------------------------
    # Generate Revised Workout Plan
    # ------------------------------------------------

    revised_plan = update_workout_plan(

        original_plan=user.original_plan,

        feedback=request_data.feedback,

        goal=user.goal,

        intensity=user.intensity
    )

    # ------------------------------------------------
    # Save Revised Plan
    # ------------------------------------------------

    updated_user = update_plan(

        user.user_id,

        revised_plan
    )

    # ------------------------------------------------
    # Show Updated Result
    # ------------------------------------------------

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "request": request,
            "user": updated_user,
            "plan": revised_plan,
            "tip": updated_user.nutrition_tip,
            "updated": True,
            "error": None
        }
    )


# ==================================================
# ADMIN / COACH DASHBOARD
# ==================================================

@router.get(
    "/view-all-users",
    response_class=HTMLResponse
)
def view_all_users(
    request: Request
):

    users = get_all_users()

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "request": request,
            "users": users
        }
    )


# ==================================================
# DELETE USER
# ==================================================

@router.post(
    "/delete-user/{user_id}"
)
def remove_user(
    user_id: str
):

    delete_user(user_id)

    return RedirectResponse(
        url="/view-all-users",
        status_code=303
    )
# ==================================================
# LOGIN
# ==================================================

@router.get(
    "/login",
    response_class=HTMLResponse
)
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "request": request
        }
    )


@router.post(
    "/login-user",
    response_class=HTMLResponse
)
def login_user(
    request: Request,
    email: str = Form(...)
):
    email = email.strip().lower()

    # Coach login
    if email == "coach@fitbuddy.com":
        return RedirectResponse(
            url="/view-all-users",
            status_code=303
        )

    # Create stable user ID from Gmail
    user_id = email.replace("@", "_at_").replace(".", "_")

    # Existing user -> personal dashboard
    user = get_user(user_id)

    if user:
        return RedirectResponse(
            url=f"/dashboard/{user.user_id}",
            status_code=303
        )

    # New user -> profile setup
    return RedirectResponse(
        url=f"/setup?email={email}",
        status_code=303
    )


# ==================================================
# NEW USER PROFILE SETUP
# ==================================================

@router.get(
    "/setup",
    response_class=HTMLResponse
)
def setup_profile(
    request: Request,
    email: str = ""
):
    email = email.strip().lower()

    user_id = (
        email
        .replace("@", "_at_")
        .replace(".", "_")
    )

    return templates.TemplateResponse(
        request=request,
        name="setup.html",
        context={
            "request": request,
            "email": email,
            "user_id": user_id
        }
    )

# ==================================================
# PERSONAL USER DASHBOARD
# ==================================================

@router.get(
    "/dashboard/{user_id}",
    response_class=HTMLResponse
)
def user_dashboard(
    request: Request,
    user_id: str
):
    user = get_user(user_id)

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
            "user": user
        }
    )
from app.gemini_generator import ask_ai_coach

# ==================================================
# AI COACH
# ==================================================

@router.post(
    "/ai-coach",
    response_class=HTMLResponse
)
def ai_coach(
    request: Request,
    user_id: str = Form(...),
    question: str = Form(...)
):
    user = get_user(user_id)

    if not user:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    answer = ask_ai_coach(
        question=question,
        username=user.username,
        goal=user.goal
    )

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
            "user": user,
            "coach_answer": answer
        }
    )


# GET /users endpoint: Retrieve all registered users (no sensitive data)
import json


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from utils.email_service import send_email, send_welcome_email, send_notification_email
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

app = FastAPI(title="Simple Email API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class EmailRequest(BaseModel):
    to_email: EmailStr
    subject: str
    message: str
    from_name: str = "Your App"

class WelcomeEmailRequest(BaseModel):
    to_email: EmailStr
    user_name: str = "User"

class NotificationEmailRequest(BaseModel):
    to_email: EmailStr
    notification_type: str = "General"
    message: str
    priority: str = "Medium"

@app.get("/")
async def root():
    return {"message": "Email API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/send-email")
async def send_email_endpoint(email_request: EmailRequest):
    try:
        result = await send_email(
            to_email=email_request.to_email,
            subject=email_request.subject,
            message=email_request.message,
            from_name=email_request.from_name
        )
        return {"success": True, "message": "Email sent successfully", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

@app.post("/send-welcome-email")
async def send_welcome_email_endpoint(request: WelcomeEmailRequest):
    """Send automated welcome email to new users"""
    try:
        result = await send_welcome_email(
            to_email=request.to_email,
            user_name=request.user_name
        )
        return {"success": True, "message": "Welcome email sent successfully", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send welcome email: {str(e)}")

@app.post("/send-notification-email")
async def send_notification_email_endpoint(request: NotificationEmailRequest):
    """Send automated notification email"""
    try:
        result = await send_notification_email(
            to_email=request.to_email,
            notification_type=request.notification_type,
            message=request.message,
            priority=request.priority
        )
        return {"success": True, "message": "Notification email sent successfully", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send notification email: {str(e)}")

import json
import uuid

@app.post("/user-signup")
async def user_signup_endpoint(request: WelcomeEmailRequest):
    """Simulate user signup, save user data, and send welcome email"""
    try:
        users_path = os.path.join(os.path.dirname(__file__), "data", "users.json")
        # Load existing users
        if os.path.exists(users_path):
            with open(users_path, "r") as f:
                try:
                    users = json.load(f)
                except Exception:
                    users = []
        else:
            users = []

        # Check if user already exists
        for user in users:
            if user.get("email") == request.to_email:
                return {
                    "success": False,
                    "message": "User already exists.",
                    "user_id": user.get("id"),
                    "user_email": user.get("email"),
                    "already_existed": True
                }

        # Create new user
        user_id = str(uuid.uuid4())
        new_user = {
            "id": user_id,
            "email": request.to_email,
            "name": request.user_name,
            "signup_time": datetime.now().isoformat()
        }
        users.append(new_user)
        # Save users
        with open(users_path, "w") as f:
            json.dump(users, f, indent=2)

        # Send welcome email automatically
        result = await send_welcome_email(
            to_email=request.to_email,
            user_name=request.user_name
        )

        return {
            "success": True,
            "message": f"User {request.user_name} signed up successfully! Welcome email sent.",
            "user_id": user_id,
            "user_email": request.to_email,
            "signup_time": new_user["signup_time"],
            "email_result": result,
            "stored": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Signup failed: {str(e)}")



@app.get("/users")
def get_users():
    users_path = os.path.join(os.path.dirname(__file__), "data", "users.json")
    if not os.path.exists(users_path):
        return []
    with open(users_path, "r") as f:
        try:
            users = json.load(f)
        except Exception:
            users = []
    # Remove any sensitive fields (if present)
    public_users = [
        {
            "id": user.get("id"),
            "email": user.get("email"),
            "name": user.get("name"),
            "signup_time": user.get("signup_time")
        }
        for user in users
    ]
    return public_users
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
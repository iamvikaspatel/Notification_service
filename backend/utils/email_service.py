import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

async def send_email(to_email: str, subject: str, message: str, from_name: str = "Your App"):
    """
    Send a custom email using SendGrid
    
    Args:
        to_email: Recipient email address
        subject: Email subject line
        message: Email body content
        from_name: Sender name
    
    Returns:
        SendGrid response
    """
    
    # Get configuration from environment
    api_key = os.getenv("SENDGRID_API_KEY")
    from_email = os.getenv("FROM_EMAIL")
    
    if not api_key:
        raise Exception("SENDGRID_API_KEY not found in environment variables")
    
    if not from_email:
        raise Exception("FROM_EMAIL not found in environment variables")
    
    # Create the email
    mail = Mail(
        from_email=(from_email, from_name),
        to_emails=to_email,
        subject=subject,
        html_content=f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px 10px 0 0; color: white;">
                        <h1 style="margin: 0; font-size: 24px;">{subject}</h1>
                    </div>
                    <div style="background-color: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; border: 1px solid #e0e0e0;">
                        <div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                            {message.replace(chr(10), '<br>')}
                        </div>
                    </div>
                    <footer style="margin-top: 20px; padding: 20px; text-align: center; color: #666; font-size: 12px; border-top: 1px solid #eee;">
                        <p>Sent from <strong>{from_name}</strong></p>
                        <p>This email was sent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
                    </footer>
                </div>
            </body>
        </html>
        """
    )
    
    try:
        # Send the email
        sg = SendGridAPIClient(api_key=api_key)
        response = sg.send(mail)
        
        return {
            "status_code": response.status_code,
            "body": response.body,
            "headers": dict(response.headers)
        }
        
    except Exception as e:
        raise Exception(f"Error sending email: {str(e)}")

async def send_welcome_email(to_email: str, user_name: str = "User"):
    """
    Send a welcome email to new users
    """
    subject = f"Welcome {user_name}! Your Account is Ready 🎉"
    
    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); padding: 30px; border-radius: 15px 15px 0 0; color: white; text-align: center;">
                    <h1 style="margin: 0; font-size: 28px;">🎉 Welcome {user_name}!</h1>
                    <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">Your account is ready to go!</p>
                </div>
                
                <div style="background-color: #f8f9fa; padding: 40px; border-radius: 0 0 15px 15px; border: 1px solid #e9ecef;">
                    <div style="background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                        <h2 style="color: #4CAF50; margin-top: 0;">Thank you for joining us!</h2>
                        
                        <p>We're excited to have you on board. Your account has been successfully created and is ready to use.</p>
                        
                        <div style="background-color: #e8f5e8; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #4CAF50;">
                            <h3 style="margin-top: 0; color: #2e7d32;">What's next?</h3>
                            <ul style="margin: 10px 0; padding-left: 20px;">
                                <li>✅ Complete your profile setup</li>
                                <li>🎯 Explore our features and tools</li>
                                <li>📞 Contact support if you need help</li>
                                <li>🚀 Start using our platform right away!</li>
                            </ul>
                        </div>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="https://yourapp.com/dashboard" 
                               style="display: inline-block; background-color: #4CAF50; color: white; padding: 15px 30px; 
                                      text-decoration: none; border-radius: 25px; font-weight: bold; font-size: 16px;">
                                Get Started Now
                            </a>
                        </div>
                        
                        <p>If you have any questions, feel free to reply to this email or contact our support team.</p>
                        
                        <p>Welcome aboard! 🚀</p>
                    </div>
                </div>
                
                <footer style="margin-top: 20px; padding: 20px; text-align: center; color: #666; font-size: 12px;">
                    <p>Sent with ❤️ from the <strong>Welcome Bot</strong></p>
                    <p>{datetime.now().strftime('%B %d, %Y at %H:%M')} UTC</p>
                    <p style="margin-top: 15px; color: #999;">
                        This is an automated welcome email. If you didn't sign up for our service, please ignore this email.
                    </p>
                </footer>
            </div>
        </body>
    </html>
    """
    
    return await _send_email_with_template(to_email, subject, html_content, "Welcome Bot")

async def send_notification_email(to_email: str, notification_type: str, message: str, priority: str = "Medium"):
    """
    Send a notification email
    """
    priority_colors = {
        "Low": "#28a745",
        "Medium": "#ffc107", 
        "High": "#dc3545",
        "Critical": "#6f42c1"
    }
    
    priority_icons = {
        "Low": "ℹ️",
        "Medium": "⚠️",
        "High": "🔴",
        "Critical": "🚨"
    }
    
    color = priority_colors.get(priority, "#ffc107")
    icon = priority_icons.get(priority, "📢")
    
    subject = f"{icon} Notification: {notification_type} - {priority} Priority"
    
    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, {color} 0%, {color}dd 100%); padding: 25px; border-radius: 10px 10px 0 0; color: white;">
                    <h1 style="margin: 0; font-size: 24px;">{icon} {notification_type}</h1>
                    <p style="margin: 5px 0 0 0; opacity: 0.9;">Priority: <strong>{priority}</strong></p>
                </div>
                
                <div style="background-color: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; border: 1px solid #e9ecef;">
                    <div style="background-color: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <div style="background-color: {color}15; border-left: 4px solid {color}; padding: 15px; margin-bottom: 20px;">
                            <h3 style="margin: 0; color: {color};">Notification Details</h3>
                        </div>
                        
                        <div style="margin: 20px 0;">
                            {message.replace(chr(10), '<br>')}
                        </div>
                        
                        <div style="background-color: #f1f3f4; padding: 15px; border-radius: 5px; margin-top: 20px;">
                            <p style="margin: 0; font-size: 12px; color: #666;">
                                <strong>Notification ID:</strong> {datetime.now().strftime('%Y%m%d%H%M%S')}<br>
                                <strong>Sent:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC<br>
                                <strong>Type:</strong> {notification_type}<br>
                                <strong>Priority:</strong> {priority}
                            </p>
                        </div>
                    </div>
                </div>
                
                <footer style="margin-top: 20px; padding: 20px; text-align: center; color: #666; font-size: 12px; border-top: 1px solid #eee;">
                    <p>This is an automated notification from the <strong>Notification System</strong></p>
                    <p>Please do not reply directly to this email.</p>
                    <p style="margin-top: 10px;">
                        For support, visit our help center or contact support@yourapp.com
                    </p>
                </footer>
            </div>
        </body>
    </html>
    """
    
    return await _send_email_with_template(to_email, subject, html_content, "Notification System")

async def _send_email_with_template(to_email: str, subject: str, html_content: str, from_name: str):
    """
    Internal function to send email with pre-built HTML template
    """
    api_key = os.getenv("SENDGRID_API_KEY")
    from_email = os.getenv("FROM_EMAIL")
    
    if not api_key:
        raise Exception("SENDGRID_API_KEY not found in environment variables")
    
    if not from_email:
        raise Exception("FROM_EMAIL not found in environment variables")
    
    mail = Mail(
        from_email=(from_email, from_name),
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )
    
    try:
        sg = SendGridAPIClient(api_key=api_key)
        response = sg.send(mail)
        
        return {
            "status_code": response.status_code,
            "body": response.body,
            "headers": dict(response.headers)
        }
        
    except Exception as e:
        raise Exception(f"Error sending email: {str(e)}")
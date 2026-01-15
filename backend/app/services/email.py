from app.config import settings

try:
    from resend import Resend
    resend_client = Resend(api_key=settings.RESEND_API_KEY) if settings.RESEND_API_KEY else None
except ImportError:
    resend_client = None


async def send_password_reset_email(email: str, reset_link: str) -> bool:
    """Send password reset email via Resend."""
    if not resend_client:
        # Log to console for development
        print(f"[DEV EMAIL] To: {email}")
        print(f"[DEV EMAIL] Reset link: {reset_link}")
        return True

    try:
        resend_client.send({
            "from": "MedBrief <noreply@medbrief.redmedai.com>",
            "to": email,
            "subject": "Reset your MedBrief password",
            "html": f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #292524; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: #E07A5F; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
                    .header h1 {{ color: white; margin: 0; }}
                    .content {{ background: #FFFBF5; padding: 30px; border: 1px solid #E7E5E4; }}
                    .button {{ display: inline-block; background: #E07A5F; color: white; padding: 14px 28px;
                              text-decoration: none; border-radius: 6px; margin: 20px 0; }}
                    .footer {{ text-align: center; padding: 20px; color: #78716C; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>MedBrief</h1>
                    </div>
                    <div class="content">
                        <h2>Password Reset Request</h2>
                        <p>You requested to reset your MedBrief password.</p>
                        <p>Click the button below to create a new password:</p>
                        <center>
                            <a href="{reset_link}" class="button">Reset Password</a>
                        </center>
                        <p>This link expires in {settings.RESET_TOKEN_EXPIRE_HOURS} hour(s).</p>
                        <p style="color: #78716C;">If you didn't request this, you can safely ignore this email.</p>
                    </div>
                    <div class="footer">
                        <p>MedBrief - Weekly signals from medical research</p>
                        <p>© 2026 MedBrief. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """
        })
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
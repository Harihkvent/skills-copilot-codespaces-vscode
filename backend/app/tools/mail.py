"""
Email sending tool
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Tuple

from app.tools.base import BaseTool, ToolResult
from app.core.config import settings


class MailSendTool(BaseTool):
    """Tool for sending emails via SMTP"""
    
    def __init__(self):
        super().__init__()
        self.name = "mail.send"
        self.description = "Send an email to one or more recipients"
        self.requires_confirmation = True
        self.parameters = {
            "type": "object",
            "properties": {
                "to": {
                    "type": "string",
                    "description": "Recipient email address"
                },
                "subject": {
                    "type": "string",
                    "description": "Email subject"
                },
                "body": {
                    "type": "string",
                    "description": "Email body content"
                },
                "cc": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "CC recipients (optional)"
                },
                "bcc": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "BCC recipients (optional)"
                }
            },
            "required": ["to", "subject", "body"]
        }
    
    def validate(self, args: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate email arguments"""
        if not args.get("to"):
            return False, "Recipient email address is required"
        if not args.get("subject"):
            return False, "Email subject is required"
        if not args.get("body"):
            return False, "Email body is required"
        
        # Check if SMTP is configured
        if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
            return False, "SMTP not configured. Please set SMTP credentials in .env file"
        
        return True, ""
    
    async def run(self, args: Dict[str, Any], user_context: Dict[str, Any]) -> ToolResult:
        """Send email via SMTP"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg["From"] = settings.SMTP_FROM or settings.SMTP_USER
            msg["To"] = args["to"]
            msg["Subject"] = args["subject"]
            
            # Add CC and BCC if provided
            if args.get("cc"):
                msg["Cc"] = ", ".join(args["cc"])
            if args.get("bcc"):
                msg["Bcc"] = ", ".join(args["bcc"])
            
            # Attach body
            msg.attach(MIMEText(args["body"], "plain"))
            
            # Connect to SMTP server and send
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
            
            return ToolResult(
                status="success",
                result={
                    "sent": True,
                    "to": args["to"],
                    "subject": args["subject"]
                }
            )
            
        except Exception as e:
            return ToolResult(
                status="failed",
                error=f"Failed to send email: {str(e)}"
            )

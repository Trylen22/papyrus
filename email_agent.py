import os
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import logging

class EmailAgent:
    SCOPES = [
        'https://www.googleapis.com/auth/gmail.send',
        'https://www.googleapis.com/auth/gmail.compose'
    ]

    def __init__(self):
        self.service = self.authenticate_gmail()

    def authenticate_gmail(self):
        """Authenticates and returns the Gmail service object."""
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secret.json', self.SCOPES)
                creds = flow.run_local_server(port=8002)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return build('gmail', 'v1', credentials=creds)

    def send_email(self, to: str, subject: str, body: str) -> bool:
        """Send an email using Gmail API"""
        try:
            logging.info(f"Attempting to send email to: {to}")
            logging.info("Checking Gmail service...")
            if not self.service:
                logging.error("Gmail service not initialized!")
                return False

            # Get sender's email
            sender_email = self.service.users().getProfile(userId='me').execute()['emailAddress']
            logging.info(f"Sending from: {sender_email}")

            message = MIMEText(body)
            message['to'] = to
            message['subject'] = subject
            message['from'] = sender_email
            
            # Log full message details
            logging.info(f"Message details:")
            logging.info(f"To: {message['to']}")
            logging.info(f"From: {message['from']}")
            logging.info(f"Subject: {message['subject']}")
            logging.info(f"Body: {body}")

            # Create the raw email
            raw = base64.urlsafe_b64encode(message.as_bytes())
            raw = raw.decode()
            
            logging.info("Email content prepared, attempting to send...")
            # Send the email
            result = self.service.users().messages().send(
                userId='me',
                body={'raw': raw}
            ).execute()
            
            logging.info(f"Email sent successfully to {to}. Message ID: {result.get('id', 'unknown')}")
            logging.info(f"Full response from Gmail API: {result}")
            return True
            
        except Exception as e:
            logging.error(f"Error sending email: {str(e)}")
            logging.error(f"Error type: {type(e)}")
            import traceback
            logging.error(f"Traceback: {traceback.format_exc()}")
            return False 
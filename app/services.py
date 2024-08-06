import smtplib
import random
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app as app

# In-memory store for OTPs and their expiry times
otp_store = {}

def generate_otp():
    """Generate a random 6-digit OTP."""
    return random.randint(100000, 999999)

def send_email_with_otp(email, receiver_email, subject, message):
    """Send an email with a 6-digit OTP."""
    otp = generate_otp()
    otp_expiry_time = time.time() + 120  # OTP expires in 120 seconds

    # Construct the email message
    email_body = f"{message}\n\nYour OTP code is: {otp}\nThis OTP will expire in 120 seconds.\n\nWith Regards,\nWallick Global Consulting"

    # Set up the email server and sender details
    password = app.config['EMAIL_PASSWORD']
    smtp_server = app.config['SMTP_SERVER']
    smtp_port = app.config['SMTP_PORT']

    # Create the email content
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(email_body, 'plain'))

    try:
        # Connect to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email, password)
            server.sendmail(email, receiver_email, msg.as_string())
            print(f"Email sent to {receiver_email} with OTP: {otp}")
    except Exception as e:
        print(f"Failed to send email: {e}")

    # Store OTP and expiry time in the dictionary
    otp_store[receiver_email] = {'otp': otp, 'expiry_time': otp_expiry_time}

    return otp, otp_expiry_time

def verify_otp_service(receiver_email, otp):
    stored_data = otp_store.get(receiver_email)

    if not stored_data:
        return {'error': 'No OTP found for this email'}

    if time.time() > stored_data['expiry_time']:
        del otp_store[receiver_email]  # Remove expired OTP
        return {'error': 'OTP has expired'}

    if int(otp) == stored_data['otp']:
        del otp_store[receiver_email]  # Remove used OTP
        return {'message': 'OTP verified successfully'}
    else:
        return {'error': 'Invalid OTP'}

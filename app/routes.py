from flask import request, jsonify, current_app as app
from .services import send_email_with_otp, verify_otp_service

@app.route('/send_otp', methods=['POST'])
def send_otp():
    data = request.json
    email = app.config['EMAIL']
    receiver_email = data.get('receiver_email')
    subject = data.get('subject', 'Your OTP Code for verification')  # Default subject
    message = data.get('message', 'Hello\nThank you for using our service.')

    if not receiver_email:
        return jsonify({'error': 'Receiver email is required'}), 400

    otp, otp_expiry_time = send_email_with_otp(email, receiver_email, subject, message)
    return jsonify({'message': 'OTP sent successfully', 'otp': otp, 'expiry_time': otp_expiry_time}), 200

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    data = request.json
    receiver_email = data.get('receiver_email')
    otp = data.get('otp')

    if not all([receiver_email, otp]):
        return jsonify({'error': 'Receiver email and OTP are required'}), 400

    result = verify_otp_service(receiver_email, otp)
    return jsonify(result), 200 if result.get('message') else 400

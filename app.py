from flask import Flask, render_template, request, redirect
from flask_mail import Mail, Message
import re
from dotenv import load_dotenv
import os
load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # SMTP server (e.g., Gmail, Outlook)
app.config['MAIL_PORT'] = 587                 # TLS Port (587) or SSL (465)
app.config['MAIL_USE_TLS'] = True             # Enable TLS (for security)
app.config['MAIL_USE_SSL'] = False            # Disable SSL (use TLS instead)
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.secret_key = os.getenv('SECRET_KEY')
app.config['MAIL_DEFAULT_SENDER'] = 'roleplay@gmail.com' 
mail = Mail(app)

pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contact/email', methods=['POST'])
def valid_email():
    msg = ''
    email = request.form.get('email')
    if not re.match(pattern, email):
        msg = 'Please. Enter a valid email!'
    else:
        pass
    return render_template('partials/validate_email.html', email=email, msg=msg)


@app.route('/contact')
def contact():
    return render_template('partials/contact.html') if  request.headers.get('HX-Request') else  render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.post('/send-mail')
def send_email():
    # Get form data
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # Create email message
    msg = Message(
        subject=f"New Contact Form Submission from {name}",
        recipients=['gianerminoespineda@gmail.com'],  # Your receiving email
        sender=email,
        # reply_to=email
    )
    # Email: {email}
    msg.body = f"""
    Name: {name}
    Email: {email}
    Message: {message}
    """
    msg.html = f"""
    <h2>New Contact Form Submission</h2>
    <p><strong>Name:</strong>{name}</p>
    <p><strong>Email:</strong>{email}</p>
    <p><strong>Message:</strong>{message}</p>
    """
    
    mail.send(msg)
    return render_template('toast.html', _message='Message sent!')

if __name__=='__main__':
    app.run()
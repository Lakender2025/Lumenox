from flask import Flask, session, render_template, request, jsonify,redirect, url_for, flash
from database import init_db, save_contact_form
from debug import logger  # Import logger for debugging
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")

# Set session lifetime
app.permanent_session_lifetime = timedelta(minutes=5)

# Initialize database connection
init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    session.permanent = True
    show_popup = request.args.get('show_popup', 'true')  # Get from URL params

    if request.method == 'POST':
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            mobile = request.form.get('mobile')
            service = request.form.get('service')
            message = request.form.get('message')

            if not all([name, email, mobile, service, message]):
                flash("All fields are required", "danger")
                return redirect(url_for('index', show_popup='true'))  # Keep popup open on error

            Subject = "Quote Based on requirement."
            save_contact_form(name, email, Subject, f"{mobile} {message} {service}")
            send_email(name, email, Subject, f"{mobile} {message} {service}")

            flash("Quote request submitted successfully!", "success")
            return redirect(url_for('index', show_popup='false'))  # Close popup after submission

        except Exception as e:
            logger.error(f"Error processing quote form: {e}")
            flash("Something went wrong", "danger")
            return redirect(url_for('index', show_popup='true'))  # Keep popup open on error

    return render_template('index.html', show_popup=(show_popup == 'true'))

# Define the project route
@app.route('/project')
def project():
    return render_template('project.html')  # Ensure you have a project.html template

# Define the project route
@app.route('/feature')
def feature():
    return render_template('feature.html')  # Ensure you have a feature.html template

# Define the project route
@app.route('/team')
def team():
    return render_template('team.html')  # Ensure you have a project.html template

from flask import render_template, request, redirect, url_for, flash

@app.route('/quote', methods=['GET', 'POST'])
def quote():
    try:
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            mobile = request.form.get('mobile')
            service = request.form.get('service')
            message = request.form.get('message')

            if not name or not email or not mobile or not service or not message:
                flash("All fields are required", "danger")  # Flash error message
                return redirect(url_for('quote'))  # Redirect back to the form

            Subject = "Quote Based on requirement."
            save_contact_form(name, email, Subject, f"{mobile} {message} {service}")

            send_email(name, email, Subject, f"{mobile} {message} {service}")

            flash("Quote request submitted successfully!", "success")  # Flash success message
            return redirect(url_for('quote'))  # Redirect to the form

        return render_template('quote.html')  # Render the form page

    except Exception as e:
        logger.error(f"Error processing quote form: {e}")
        flash("Something went wrong", "danger")  # Flash error message
        return redirect(url_for('quote'))  # Redirect to the form

# Error Page
@app.route('/error')
def error_page():
    return render_template('error.html')

@app.route('/error')
def error_404():
    return render_template('error.html')

# Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('error_page'))

@app.errorhandler(500)
def internal_server_error(e):
    logger.error(f"Internal Server Error: {e}")
    flash("An unexpected error occurred. Please try again later.", "danger")
    return redirect(url_for('error_page'))


# @app.route('/close-popup')
# def close_popup():
#     # index('false')
#     return render_template('index.html', show_popup='False')  # Hide popup

@app.route('/popup-page')
def popup_page():
    return render_template('popup.html')  # Or the correct template you want to render

# About Page
@app.route('/about')
def about():
    return render_template('about.html')

# Testimonials Page
@app.route('/testimonial')
def testimonial():
    return render_template('testimonial.html')

# News Page
@app.route('/news')
def news():
    return render_template('news.html')

# Services Page
@app.route('/service')
def service():
    return render_template('service.html')

# Contact Page with Form Handling
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            subject = request.form.get('subject')
            message = request.form.get('message')

            if not name or not email or not message:
                flash("All fields are required!", "danger")
                return redirect(url_for('contact'))

            # Save to database
            save_contact_form(name, email,subject, message)

            # Send email notification
            send_email(name, email, subject, message)


            flash("Your message has been sent successfully!", "success")
            return redirect(url_for('contact'))

        except Exception as e:
            logger.error(f"Error processing contact form: {e}")
            flash("Something went wrong. Please try again later.", "danger")
            return redirect(url_for('error_page'))

    return render_template('contact.html')


# Function to Send Email
def send_email(name, email, subject, message):
    try:
        sender_email = os.getenv("EMAIL_USER")
        sender_password = os.getenv("EMAIL_PASS")
        receiver_email = os.getenv("RECEIVER_EMAIL")

        # Create the email content
        msg = MIMEText(f"Name: {name}\nEmail: {email}\nSubject: {subject}\nMessage: {message}")
        msg["Subject"] = "Lumenox : "+subject
        msg["From"] = sender_email
        msg["To"] = receiver_email

        # Send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            logger.error('Sent Successfully')

    except Exception as e:
        logger.error(f"Error sending email: {e}")
@app.route('/submit-survey', methods=['POST'])
def submit_survey():
    try:
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            interest = request.form.get('interest')

            if not all([name, email, phone, interest]):
                flash("All fields are required", "danger")
                return redirect(url_for('index', show_popup='true'))  # Keep popup open on error

            subject = "Important! - Pop Up Mail."
            print(f"Survey submitted: {name}, {email}, {phone}, {interest}")
            send_email(name, email, subject, interest)
            save_contact_form(name, email, subject, interest)

            flash("Survey submitted successfully!", "success")
            return redirect(url_for('index', show_popup='false'))  # Close popup after submission

    except Exception as e:
        logger.error(f"Error processing survey form: {e}")
        flash("Something went wrong", "danger")
        return redirect(url_for('index', show_popup='true'))  # Keep popup open on error

if __name__ == "__main__":
    app.run(debug=True)
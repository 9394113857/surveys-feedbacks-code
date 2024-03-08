from flask import Flask, render_template, request
import sqlite3
from datetime import datetime, date
import os
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# Function to insert response into the 'responses' table
def insert_response(name, email, feedback, rating):
    conn = sqlite3.connect('survey_feedback.db')
    c = conn.cursor()
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO responses (name, email, feedback, rating, date, time) VALUES (?, ?, ?, ?, ?, ?)",
              (name, email, feedback, rating, date_time.split()[0], date_time.split()[1]))
    conn.commit()
    conn.close()

# Function to fetch all survey records from the 'responses' table
def fetch_survey_records():
    conn = sqlite3.connect('survey_feedback.db')
    c = conn.cursor()
    c.execute("SELECT * FROM responses")
    survey_records = c.fetchall()
    conn.close()
    return survey_records

# Function to insert feedback into the 'feedbacks' table
def insert_feedback(feedback):
    conn = sqlite3.connect('survey_feedback.db')
    c = conn.cursor()
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO feedbacks (feedback, date, time) VALUES (?, ?, ?)", 
              (feedback, date_time.split()[0], date_time.split()[1]))
    conn.commit()
    conn.close()

# Function to fetch all feedback records from the 'feedbacks' table
def fetch_feedback_records():
    conn = sqlite3.connect('survey_feedback.db')
    c = conn.cursor()
    c.execute("SELECT * FROM feedbacks")
    feedback_records = c.fetchall()
    conn.close()
    return feedback_records

# Route to render the survey form HTML template
@app.route('/')
def survey_form():
    return render_template('survey_form.html')

# Route to handle form submission for the survey
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Extract data from the submitted form
        name = request.form['name']
        email = request.form['email']
        feedback = request.form['feedback']
        rating = request.form['rating']
        # Insert the response into the 'responses' table
        insert_response(name, email, feedback, rating)
        # Log the submission
        logger.info(f"Survey response received from {name} with email {email} and rating {rating}")
        # Return a confirmation message
        return 'Thank you for your response!'

# Route to view survey records
@app.route('/view_survey_records')
def view_survey_records():
    survey_records = fetch_survey_records()
    return render_template('view_survey_records.html', survey_records=survey_records)

# Route to render the feedback form HTML template
@app.route('/feedback')
def feedback_form():
    return render_template('feedback_form.html')

# Route to handle form submission for feedback
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    if request.method == 'POST':
        feedback = request.form['feedback']
        # Insert the feedback into the 'feedbacks' table
        insert_feedback(feedback)
        # Log the feedback
        logger.info(f"Feedback received: {feedback}")
        # Return a confirmation message
        return 'Thank you for your feedback!'

# Route to view feedback records
@app.route('/view_feedback_records')
def view_feedback_records():
    feedback_records = fetch_feedback_records()
    return render_template('view_feedback_records.html', feedback_records=feedback_records)

if __name__ == '__main__':
    # Set up logger configuration
    logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    
    # Get the current year and month
    current_year = date.today().strftime('%Y')
    current_month = date.today().strftime('%m')
    current_day = date.today().strftime('%d')
    
    # Create directories for the current year, month, and day
    year_month_day_dir = os.path.join(logs_dir, current_year, current_month, current_day)
    os.makedirs(year_month_day_dir, exist_ok=True)
    
    # Define the log file name using today's date
    log_file = os.path.join(year_month_day_dir, 'app.log')
    
    # Create a RotatingFileHandler with log file rotation settings
    log_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=5)
    log_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s [%(module)s:%(lineno)d] %(message)s'))
    
    # Create a logger and set its level to INFO
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    # Add the RotatingFileHandler to the logger
    logger.addHandler(log_handler)
    
    # Run the Flask application
    app.run(debug=True)

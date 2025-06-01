from flask import Flask, render_template, request, redirect, url_for # type: ignore
import calendar as cal
from datetime import datetime, date, timedelta
from collections import defaultdict

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'your_secret_key'  # Needed for flash messages

@app.route('/', methods=['GET'])
def index():
    selected_month = request.args.get('attendance-month')  # format YYYY-MM
    attendance_data = {
        '2025-06-01': 'Present',
        '2025-06-02': 'Absent',
        '2025-06-03': 'Present',
        '2025-06-04': 'Present',
        '2025-06-05': 'Present',
        '2025-06-06': 'Holiday',
        '2025-06-07': 'Event',
        # Add more dates as needed
    }

    calendar_matrix = []
    if selected_month:
        # Parse year and month
        try:
            year, month = map(int, selected_month.split('-'))
            # Generate calendar weeks for the month
            month_calendar = cal.Calendar(firstweekday=6).monthdatescalendar(year, month)
            # monthdatescalendar returns list of weeks, each week is a list of 7 date objects
            # We will pass this directly to template, but replace dates outside month with None
            calendar_matrix = []
            for week in month_calendar:
                week_days = []
                for day in week:
                    if day.month == month:
                        week_days.append(day)
                    else:
                        week_days.append(None)
                calendar_matrix.append(week_days)
        except Exception as e:
            selected_month = None
    subjects = ['Math', 'Science', 'English', 'Social Studies']

    # Get selected subject from query params
    selected_subject = request.args.get('subject', 'overall')

    # Example performance data structure
    performance_data = {
        'overall': {
            'Daily Tests': 85,
            'Weekly Tests': 91,
            'Monthly Tests': 78,
            'Semester': 88,
            'Prefinals': 92,
            'Finals': 95,
        },
        'Math': {
            'Daily Tests': 90,
            'Weekly Tests': 93,
            'Monthly Tests': 80,
            'Semester': 89,
            'Prefinals': 94,
            'Finals': 97,
        },
        'Science': {
            'Daily Tests': 82,
            'Weekly Tests': 87,
            'Monthly Tests': 75,
            'Semester': 85,
            'Prefinals': 90,
            'Finals': 92,
        },
        'English': {
            'Daily Tests': 84,
            'Weekly Tests': 89,
            'Monthly Tests': 77,
            'Semester': 86,
            'Prefinals': 91,
            'Finals': 93,
        },
        'Social Studies': {
            'Daily Tests': 88,
            'Weekly Tests': 90,
            'Monthly Tests': 79,
            'Semester': 87,
            'Prefinals': 93,
            'Finals': 96,
        }
    }

    # Get the performance scores for the selected subject
    performance_scores = performance_data.get(selected_subject, performance_data['overall'])

    # ... calendar logic as before ...

    return render_template(
        'students.html',
        selected_month=selected_month,
        calendar=calendar_matrix,
        attendance_data=attendance_data,
        subjects=subjects,
        selected_subject=selected_subject,
        performance_scores=performance_scores
    )

@app.route('/feedback', methods=['POST'])
def feedback():
    subject = request.form.get('subject')
    message = request.form.get('message')
    # Here you can save to a database or send an email. For demo, just print:
    print(f"Feedback received: Subject: {subject}, Message: {message}")
    # flash("Thank you for your feedback/query!")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

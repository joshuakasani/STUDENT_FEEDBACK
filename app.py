from flask import Flask, request ,render_template, redirect
import mysql.connector
from config import db_config

app = Flask(__name__)

def get_db_connection():
    """Establish a database connection."""
    return mysql.connector.connect(**db_config)
@app.route('/')
def index():
    """Render the feedback form."""
    return render_template('index.html')


@app.route('/feedback', methods=['GET','POST'])
def feedback():
    """Handle feedback submission."""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        comment = request.form['comment']

        # Save feedback to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO feedback (student_name, email, comments) VALUES (%s, %s, %s)",
            (name, email, comment)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/')
    return render_template('feedback.html')
@app.route('/admin')
def admin():
    """Render the admin page with feedback data."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM feedback ORDER BY submitted_at DESC")
    feedbacks = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('admin.html', feedbacks=feedbacks)

if __name__ == '__main__':
    app.run(debug=True)


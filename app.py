import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Function to create a database connection
def create_connection():
    return sqlite3.connect('fitness_app.db')

# Function to create the workouts table (if it doesn't already exist)
def create_table(conn):
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS workouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exercise TEXT NOT NULL,
        sets INTEGER NOT NULL,
        reps INTEGER NOT NULL,
        weight INTEGER NOT NULL,
        date TEXT NOT NULL
    )
    ''')
    conn.commit()

# Route for the homepage that shows all workouts
@app.route('/')
def index():
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM workouts')
    workouts = c.fetchall()
    conn.close()
    return render_template('index.html', workouts=workouts)

# Route to add a new workout log
@app.route('/add', methods=['GET', 'POST'])
def add_workout():
    if request.method == 'POST':
        exercise = request.form['exercise']
        sets = request.form['sets']
        reps = request.form['reps']
        weight = request.form['weight']
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Corrected line
        
        conn = create_connection()
        c = conn.cursor()
        c.execute('''
        INSERT INTO workouts (exercise, sets, reps, weight, date)
        VALUES (?, ?, ?, ?, ?)
        ''', (exercise, sets, reps, weight, date))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('add_workout.html')

@app.route('/delete/<int:workout_id>', methods=['POST'])
def delete_workout(workout_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('DELETE FROM workouts WHERE id = ?', (workout_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Create the database and table if they don't exist
    conn = create_connection()
    create_table(conn)
    conn.close()

    # Run the Flask application
    app.run(debug=True)
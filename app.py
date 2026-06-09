# app.py
"""
Flask backend for portfolio website.
Handles routing, contact form submissions, and SQLite database storage.
"""
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, g
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'  # Required for flashing messages

DATABASE = 'database.db'

def get_db():
    """Get database connection."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Close database connection."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """Initialize SQLite database with messages table."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    db.commit()

# Initialize database when app starts
with app.app_context():
    init_db()

# Routes
@app.route('/')
def home():
    """Home page route."""
    return render_template('index.html')

@app.route('/about')
def about():
    """About page route."""
    return render_template('about.html')

@app.route('/projects')
def projects():
    """Projects page route."""
    return render_template('projects.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page route with form handling."""
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        
        # Basic validation
        if not name or not email or not subject or not message:
            flash('Please fill in all fields.', 'error')
        elif '@' not in email or '.' not in email:
            flash('Please enter a valid email address.', 'error')
        else:
            # Store in database
            db = get_db()
            db.execute(
                'INSERT INTO messages (name, email, subject, message) VALUES (?, ?, ?, ?)',
                (name, email, subject, message)
            )
            db.commit()
            flash('Thank you! Your message has been sent successfully.', 'success')
            return redirect(url_for('contact'))
    
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
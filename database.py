import sqlite3
import json
from datetime import datetime

def init_database():
    conn = sqlite3.connect('interview_assistant.db')
    c = conn.cursor()

    # Create candidates table
    c.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            experience_years INTEGER,
            desired_position TEXT,
            location TEXT,
            tech_stack TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create interviews table
    c.execute('''
        CREATE TABLE IF NOT EXISTS interviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER,
            questions TEXT,
            answers TEXT,
            score FLOAT,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (candidate_id) REFERENCES candidates (id)
        )
    ''')

    conn.commit()
    conn.close()

def save_candidate(candidate_data):
    conn = sqlite3.connect('interview_assistant.db')
    c = conn.cursor()

    try:
        # First check if email exists
        c.execute('SELECT id FROM candidates WHERE email = ?', (candidate_data['email'],))
        if c.fetchone() is not None:
            conn.close()
            return None

        c.execute('''
            INSERT INTO candidates 
            (full_name, email, phone, experience_years, desired_position, location, tech_stack)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            candidate_data['full_name'],
            candidate_data['email'],
            candidate_data['phone'],
            candidate_data['experience_years'],
            candidate_data['desired_position'],
            candidate_data['location'],
            json.dumps(candidate_data['tech_stack'])
        ))

        candidate_id = c.lastrowid
        conn.commit()

        # Fetch candidate details
        c.execute('SELECT * FROM candidates WHERE id = ?', (candidate_id,))
        candidate = c.fetchone()
        return candidate_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def get_candidate_by_id(candidate_id):
    conn = sqlite3.connect('interview_assistant.db')
    c = conn.cursor()

    c.execute('''
        SELECT full_name, desired_position, tech_stack
        FROM candidates
        WHERE id = ?
    ''', (candidate_id,))

    result = c.fetchone()
    conn.close()

    if result:
        return {
            'full_name': result[0],
            'desired_position': result[1],
            'tech_stack': json.loads(result[2])
        }
    return None

def save_interview(interview_data):
    conn = sqlite3.connect('interview_assistant.db')
    c = conn.cursor()

    c.execute('''
        INSERT INTO interviews 
        (candidate_id, questions, answers, score, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        interview_data['candidate_id'],
        json.dumps(interview_data['questions']),
        json.dumps(interview_data['answers']),
        interview_data['score'],
        interview_data['status']
    ))

    conn.commit()
    conn.close()

def get_candidate_interviews():
    conn = sqlite3.connect('interview_assistant.db')
    c = conn.cursor()

    c.execute('''
        SELECT 
            c.full_name,
            c.email,
            c.tech_stack,
            i.score,
            i.status,
            i.created_at
        FROM interviews i
        JOIN candidates c ON i.candidate_id = c.id
        ORDER BY i.created_at DESC
    ''')

    results = c.fetchall()
    conn.close()

    return results
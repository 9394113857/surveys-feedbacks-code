import sqlite3

def create_tables():
    print("\nCreating tables...")
    conn = sqlite3.connect('survey_feedback.db')
    c = conn.cursor()

    # Check if 'responses' table exists
    c.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='responses' ''')
    if c.fetchone()[0]==1 :
        print('Table responses already exists.')
    else:
        # Create 'responses' table if it doesn't exist
        c.execute('''CREATE TABLE responses
                     (id INTEGER PRIMARY KEY, name TEXT, email TEXT, feedback TEXT, rating INTEGER, date TEXT, time TEXT)''')
        print('Table responses created.')

    # Check if 'feedbacks' table exists
    c.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='feedbacks' ''')
    if c.fetchone()[0]==1 :
        print('Table feedbacks already exists.')
    else:
        # Create 'feedbacks' table if it doesn't exist
        c.execute('''CREATE TABLE feedbacks
                     (id INTEGER PRIMARY KEY, feedback TEXT, date TEXT, time TEXT)''')
        print('Table feedbacks created.')

    conn.commit()
    conn.close()

def check_tables():
    print("\nChecking existing tables...")
    conn = sqlite3.connect('survey_feedback.db')
    c = conn.cursor()

    # Check if 'responses' table exists
    c.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='responses' ''')
    if c.fetchone()[0]==1 :
        print('Table responses exists.')
    else:
        print('Table responses does not exist.')

    # Check if 'feedbacks' table exists
    c.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='feedbacks' ''')
    if c.fetchone()[0]==1 :
        print('Table feedbacks exists.')
    else:
        print('Table feedbacks does not exist.')

    conn.close()

if __name__ == '__main__':
    create_tables()
    check_tables()

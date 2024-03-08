import sqlite3

def drop_tables():
    print("Connecting to the database...")
    conn = sqlite3.connect('survey_feedback.db')
    print("Connected successfully.")

    c = conn.cursor()

    # Check if 'responses' table exists
    c.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='responses' ''')
    if c.fetchone()[0] == 1:
        # Drop 'responses' table
        print("\nDropping 'responses' table...")
        c.execute("DROP TABLE responses")
        print("Table 'responses' dropped successfully.")
    else:
        print("\nTable 'responses' does not exist. Skipping.")

    # Check if 'feedbacks' table exists
    c.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='feedbacks' ''')
    if c.fetchone()[0] == 1:
        # Drop 'feedbacks' table
        print("\nDropping 'feedbacks' table...")
        c.execute("DROP TABLE feedbacks")
        print("Table 'feedbacks' dropped successfully.")
    else:
        print("\nTable 'feedbacks' does not exist. Skipping.")

    conn.commit()
    conn.close()
    print("Connection closed.")

if __name__ == '__main__':
    drop_tables()

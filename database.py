import sqlite3

def init_db():
    conn = sqlite3.connect("storage.db")
    cursor = conn.cursor()

    # Create the slots table if it doesn't already exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS slots (
            id INTEGER PRIMARY KEY,
            status TEXT DEFAULT 'available',
            name TEXT DEFAULT '',
            date TEXT DEFAULT ''
        )
    """)

    #table slots
    cursor.execute("SELECT COUNT(*) FROM slots")
    if cursor.fetchone()[0] == 0:
        for i in range(1, 33):  # Insert 32 slots
            cursor.execute("INSERT INTO slots (id, status) VALUES (?, 'available')", (i,))

    conn.commit()
    conn.close()


def get_slots():
    conn = sqlite3.connect("storage.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM slots")
    slots = cursor.fetchall()
    conn.close()
    return slots

def update_slot(slot_id, new_status, name="", date=""):
    conn = sqlite3.connect("storage.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE slots 
        SET status = ?, name = ?, date = ? 
        WHERE id = ?
    """, (new_status, name, date, slot_id))
    conn.commit()
    conn.close()

    print(f"Slot {slot_id} updated: Status = {new_status}, Name = {name}, Date = {date}")  # Debugging line

    
    # confirmation
    print(f"Updated Slot {slot_id}: Status = {new_status}, Name = {name}, Date = {date}")


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")


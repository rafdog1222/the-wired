from database import get_connections
from datetime import datetime 

def write_entry(email, address, title, content): 
    conn = get_connections()
    cursor = conn.cursor()

    cursor.execute(
            "SELECT id FROM library WHERE author_email = %s AND title = %s",
            (email, title)
        )

    existing = cursor.fetchone()

    if existing: 
        print("you already have an entry with that title in this library")
        conn.close()
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    cursor.execute(
            "INSERT INTO library (origin_address, author_email, title, content, timestamp) VALUES (%s, %s, %s, %s, %s)",
            (address, email, title, content, timestamp)
        )


    conn.commit()
    conn.close()
    print(f"entry '{title}' saved to the library")

def read_library(address):
    conn = get_connections()
    cursor = conn.cursor()

    cursor.execute(
            "SELECT author_email, title, content, timestamp FROM library WHERE origin_address = %s ORDER BY timestamp DESC",
            (address,)
        )

    entries = cursor.fetchall()
    conn.close()

    if not entries:
        print("the library is empty.. leave something behind")
        return

    print(f"\n--- library of {address} ---")
    for entry in entries:
        print(f"\n[{entry[3]}] {entry[0]}")
        print(f"title: {entry[1]}")
        print(f"{entry[2]}")
    print("\n--- end of library ---")

# I think I am understanding the flow of nvim now..

def read_entry(address, title):
    conn = get_connections()
    cursor = conn.cursor()

    cursor.execute(
            "SELECT author_email, title, content, timestamp FROM library WHERE origin_address = %s AND title =%s",
            (address, title)
        )

    entry = cursor.fetchone()
    conn.close()

    if not entry:
        print("no entry found with that title")
        return

    print(f"\n[{entry[3]}] {entry[0]}")
    print(f"title: {entry[1]}")
    print(f"\n{entry[2]}")


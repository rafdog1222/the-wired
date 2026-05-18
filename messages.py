from database import get_connections
from datetime import datetime

def post_message(email, address, content):
    conn = get_connections()
    cursor = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    cursor.execute(
            "INSERT INTO messages (origin_address, author_email, content, timestamp) VALUES (%s, %s, %s, %s)",
            (address, email, content, timestamp)
        )

    conn.commit()
    conn.close()
    print("messages posted to the board")

def read_message(address):
    conn = get_connections()
    cursor = conn.cursor()

    cursor.execute(
            "SELECT author_email, content, timestamp FROM messages WHERE origin_address = %s ORDER BY timestamp DESC",
            (address,)
        )

    messages = cursor.fetchall()
    conn.close()

    if not messages: 
        print("the board is quite... be the first to post something..")
        return

    print(f"\n--- message board for {address} ---")
    for msg in messages:
        print(f"[{msg[2]}] {msg[0]}")
        print(f"{msg[1]}")
    print("\n--- end of board ---")


from database import get_connections 

# this was the travel and reading feature I was talking about in the readme...

def get_prefix(address, level):
    parts = address.split("-")
    if level == 0:
        return "#0"
    elif level == 1:
        return f"#0-{parts[1]}"
    elif level == 2:
        return f"#0-{parts[1]}-{parts[2]}"
    else:
        return address


def view_messages_at_level(address, level):
    conn = get_connections()
    cursor = conn.cursor()

    prefix = get_prefix(address, level)
    level_names = ["core hub", "sub-core", "city", "district"]

    cursor.execute(
            "SELECT origin_address, author_email, content, timestamp FROM messages WHERE origin_address LIKE ? ORDER BY timestamp DESC LIMIT 20",
            (f"{prefix}%",)
        )

    messages = cursor.fetchall()
    conn.close()

    if not messages:
        print(f"\nno messages flowing through {level_names[level]}...")
        return

    print(f"\n--- {level_names[level]} feed {prefix} ---")
    for msg in messages:
        print(f"\n[{msg[3]}] {msg[1]} from {msg[0]}")
        # Dream by Sunsat (if you see this you are obligated to listen now..)
        print(f"{msg[2]}")
    print(f"\n--- end of feed ---")


def view_library_at_level(address, level):
    conn = get_connections()
    cursor = conn.cursor()

    prefix = get_prefix(address, level)
    level_names = ["core hub", "sub-core", "city", "districts"]

    cursor.execute(
            "SELeCT origin_address, author_email, title, timestamp FROM library WHERE origin_address LIKE ? ORDER BY timestamp DESC", 
            (f"{prefix}%",)
        )

    entries = cursor.fetchall()
    conn.close()

    if not entries:
        print(f"\nno entries in the {level_names[level]} library...")
        return

    print(f"\n--- {level_names[level]} library {prefix} ---")
    for entry in entries:
        print(f"[{entry[3]}] {entry[1]} - '{entry[2]}' from {entry[0]}")
    print(f"\n-- end of library ---")

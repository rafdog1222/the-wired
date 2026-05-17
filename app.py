from flask import Flask, render_template, request, redirect, session
from district import assign_member
from database import get_connections
from messages import post_message, read_message
from library import write_entry, read_library, read_entry
from travel import view_messages_at_level, view_library_at_level
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "wired-secret-change-this-later"

def get_member(email):
    conn = get_connections()
    cursor = conn.cursor()
    cursor.execute(
            "SELECT address FROM members WHERE email = ?", 
            (email,)
    )
    member = cursor.fetchone()
    conn.close()
    return member 


@app.route("/", methods=["GET", "POST"])
def index():
    if "email" in session:
        return redirect("/district")
    if request.method == "POST":
        email = request.form["email"]
        member = get_member(email)
        if not member:
            assign_member(email)
        session["email"] = email
        return redirect("/district")
    return render_template("index.html")

# either a; that works, or b; it fails and I have to rewrite it..
# spoiler it was b, then b, then b, then a! Yippeee!!

@app.route("/district")
def districts(): 
    if "email" not in session:
        return redirect("/")
    email = session["email"]
    member = get_member(email)
    address = member[0]
    return render_template("district.html", email=email, address=address)

# I LOVE Kabuki-Cho by Kirinji

@app.route("/messages")
def messages():
    if "email" not in session:
        return redirect("/")
    email = session["email"]
    member = get_member(email)
    address = member[0]
    conn = get_connections()
    cursor = conn.cursor()
    status = get_or_create_travel(cursor, email)
    current_level = status[0]
    parts = address.split("-")
    if current_level == 0:
        prefix = "#0"
    elif current_level == 1:
        prefix = f"#0-{parts[1]}"
    elif current_level == 2:
        prefix = f"#0-{parts[1]}-{parts[2]}"
    else:
        prefix = address
    level_names = ["core hub", "sub-core", "city", "your district"]
    cursor.execute(
        "SELECT author_email, content, timestamp, origin_address FROM messages WHERE origin_address LIKE ? ORDER BY timestamp DESC",
        (f"{prefix}%",)
    )
    msgs = cursor.fetchall()
    conn.commit()
    conn.close()
    return render_template("messages.html",
        email=email,
        address=address,
        messages=msgs,
        level_name=level_names[current_level],
        prefix=prefix
    )


@app.route("/post_message", methods=["POST"])
def post_message_route():
    if "email" not in session:
        return redirect("/")
    email = session["email"]
    member = get_member(email)
    address = member[0]
    content = request.form["content"]
    if content.strip():
        post_message(email, address, content)
    return redirect("/messages")

# DANCE ALONE by The Vanished People & Hashimero
# we be listing to all the music!! 

@app.route("/library")
def library():
    if "email" not in session:
        return redirect("/")
    email = session["email"]
    member = get_member(email)
    address = member[0]
    conn = get_connections()
    cursor = conn.cursor()
    status = get_or_create_travel(cursor, email)
    current_level = status[0]
    parts = address.split("-")
    if current_level == 0:
        prefix = "#0"
    elif current_level == 1:
        prefix = f"#0-{parts[1]}"
    elif current_level == 2:
        prefix = f"#0-{parts[1]}-{parts[2]}"
    else:
        prefix = address
    level_names = ["core hub", "sub-core", "city", "your district"]
    cursor.execute(
        "SELECT id, author_email, title, timestamp, origin_address FROM library WHERE origin_address LIKE ? ORDER BY timestamp DESC",
        (f"{prefix}%",)
    )
    entries = cursor.fetchall()
    conn.commit()
    conn.close()
    return render_template("library.html",
        email=email,
        address=address,
        entries=entries,
        level_name=level_names[current_level],
        prefix=prefix
    )

@app.route("/library/<int:entry_id>")
def library_entry(entry_id):
    if "email" not in session:
        return redirect("/")
    email = session["email"]
    member = get_member(email)
    address = member[0]
    conn = get_connections()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT author_email, title, content, timestamp, origin_address FROM library WHERE id = ?",
        (entry_id,)
    )
    entry = cursor.fetchone()
    conn.close()
    if not entry:
        return redirect("/library")
    return render_template("entry.html", email=email, address=address, entry=entry)

# should i keep telling my music? 
# ahh, why not..
# Member of the Cast by Midnight City Music 
# also join the discord in the readme, you code goblin.. 

@app.route("/write", methods=["GET", "POST"])
def write():
    if "email" not in session:
        return redirect("/")
    email = session["email"]
    member = get_member(email)
    address = member[0] 
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        if title.strip() and content.strip():
            write_entry(email, address, title, content)
        return redirect("/library")
    return render_template("write.html", email=email, address=address)


@app.route("/citizens")
def citizens():
    if "email" not in session:
        return redirect("/")
    conn = get_connections()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT email, address, joined_date FROM members ORDER BY joined_date ASC"
    )
    all_members = cursor.fetchall()
    conn.close()
    return render_template("citizens.html", members=all_members)


# helpers for the travel up & down bugs

def get_or_create_travel(cursor, email): 

    cursor.execute(
        "SELECT current_level, travel_started, destination_level FROM travel WHERE email = ?",
        (email,)
    )
    status = cursor.fetchone()
    if not status:
        cursor.execute(
            "INSERT INTO travel (email, current_level, travel_started, destination_level) VALUES (?, 3, NULL, NULL)",
            (email,)
        )
        return (3, None, None)
    return status


@app.route("/travel")
def travel():
    if "email" not in session:
        return redirect("/")
    email = session["email"]
    member = get_member(email)
    address = member[0]
    conn = get_connections()
    cursor = conn.cursor()
    status = get_or_create_travel(cursor, email)
    now = datetime.now()
    travelling = False
    seconds_left = 0
    destination_level = None
    current_level = status[0]

    if status[1] and status[2] is not None:
        started = datetime.fromisoformat(status[1])
        arrive_at = started + timedelta(seconds=5)
        destination_level = status[2]
        if now < arrive_at:
            travelling = True
            seconds_left = int((arrive_at - now).total_seconds())
        else:
            current_level = status[2]
            cursor.execute(
                "UPDATE travel SET current_level = ?, travel_started = NULL, destination_level = NULL WHERE email = ?",
                (current_level, email)
            )

    conn.commit()
    conn.close()
    level_names = ["core hub", "sub-core", "city", "district"]
    return render_template("travel.html",
        email=email,
        address=address,
        current_level=current_level,
        level_names=level_names,
        travelling=travelling,
        seconds_left=seconds_left,
        destination_level=destination_level
    )



@app.route("/travel/go/<int:destination>")
def travel_go(destination):
    if "email" not in session:
        return redirect("/")
    email = session["email"]
    conn = get_connections()
    cursor = conn.cursor()
    status = get_or_create_travel(cursor, email)
    current_level = status[0]

    if status[1] is not None:
        conn.close()
        return redirect("/travel")

    if abs(destination - current_level) != 1:
        conn.close()
        return redirect("/travel")

    now = datetime.now().isoformat()
    cursor.execute(
        "INSERT OR REPLACE INTO travel (email, current_level, travel_started, destination_level) VALUES (?, ?, ?, ?)",
        (email, current_level, now, destination)
    )
    conn.commit()
    conn.close()
    return redirect("/travel")




@app.route("/travel/messages")
def travel_messages():
    if "email" not in session:
        return redirect("/")
    email = session["email"]
    member = get_member(email)
    address = member[0]
    conn = get_connections()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT current_level FROM travel WHERE email = ?", 
        (email,)
    )
    status = cursor.fetchone()
    current_level = status[0]if status else 3 
    conn.close()
    msgs = []
    # big guns time.. 
    conn = get_connections()
    cursor = conn.cursor()
    parts = address.split("-")
    if current_level == 0:
        prefix = "#0"
    elif current_level == 1:
        prefix = f"#0-{parts[1]}"
    elif current_level == 2:
        prefix = f"#0-{parts[1]}-{parts[2]}"
    else:
        prefix = address
    cursor.execute(
        "SELECT origin_address, author_email, content, timestamp FROM messages WHERE origin_address LIKE ? ORDER BY timestamp DESC LIMIT 30",
        (f"{prefix}%",)
    )
    msgs = cursor.fetchall()
    conn.close() 
    level_names = ["core hub", "sub-core", "city", "district"]
    return render_template("travel_messages.html",
        email=email,
        address=address,
        messages=msgs,
        current_level=current_level,
        level_name=level_names[current_level],
        prefix=prefix
    )

# i was about to say hastag, but that would be useles, so read the next line like "hastag" insted of "hash"
# logging out yippe! 
@app.route("/logout")
def logout():
    session.clear() 
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

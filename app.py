import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, session
from district import assign_member
from database import get_connections
from messages import post_message, read_message
from library import write_entry, read_library, read_entry
from travel import view_messages_at_level, view_library_at_level
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from filter import blur_bad_words, contains_bad_words


app = Flask(__name__)

load_dotenv()

app.secret_key = os.getenv("SECRET_KEY", "fallback-dev-key")


def get_member(email):
    conn = get_connections()
    cursor = conn.cursor()
    cursor.execute(
            "SELECT address FROM members WHERE email = %s", 
            (email,)
    )
    member = cursor.fetchone()
    conn.close()
    return member 


@app.route("/", methods=["GET", "POST"])
def index():
    if "email" in session:
        return redirect("/district")
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "email" in session:
        return redirect("/district")
    error = None 
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        confirm = request.form["confirm"]

        if not email or not password:
            error = "email and password are required"
        elif len(password) < 3: 
            error = "password must be at least 3 charcters"
        elif password != confirm:
            error = "passwords do not match"
        else:
            conn = get_connections()
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM members WHERE email = %s", (email,))
            existing = cursor.fetchone()
            if existing:
                error = "that email is already in the wired.." 
                conn.close()
            else:
                password_hash  = generate_password_hash(password)
                assign_member(email)
                cursor.execute(
                    "UPDATE members SET password_hash = %s WHERE email = %s",
                    (password_hash, email)
                )
                conn.commit()
                conn.close()
                session["email"] = email
                return redirect("/district")
    return render_template("signup.html", error=error)



@app.route("/login", methods=["GET", "POST"])
def login():
    if "email" in session:
        return redirect("/district")
    error = None
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        conn = get_connections()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT password_hash, filter_on FROM members WHERE email = %s",
            (email,)
        )
        member = cursor.fetchone()
        conn.close()
        # why does water taste so.. weird.. fuck i love and hate water..
        if not member or not member[0]:
            error = "email not found"
        elif not check_password_hash(member[0], password):
            error = "wrong password.."
        else:
            session["email"] = email
            # member[1] = filter_on
            session["filter"] = (
                member[1] if member[1] is not None else True
            )

            return redirect("/district")
    return render_template("login.html", error=error)

# either a; that works, or b; it fails and I have to rewrite it..
# spoiler it was b, then b, then b, then a! Yippeee!!

@app.route("/district")
def districts(): 
    if "email" not in session:
        return redirect("/")
    email = session["email"]
    member = get_member(email)
    if member is None:
        return "member not found", 404
    address = member[0]
    
    filter_on = session.get("filter", True)
    if "filter" not in session:
        session["filter"] = True
    return render_template("district.html", email=email, address=address, filter_on=filter_on)

# I LOVE Kabuki-Cho by Kirinji

@app.route("/toggle_filter")
def toggle_filter():
    if "email" not in session:
        return redirect("/")
    email = session["email"]
    current = session.get("filter", True)
    new_val = not current
    session["filter"] = new_val
    conn = get_connections()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE members SET filter_on = %s WHERE email = %s",
        (new_val, email)
    )
    conn.commit()
    conn.close()
    return redirect(request.referrer or "/district")


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
        "SELECT author_email, content, timestamp, origin_address FROM messages WHERE origin_address LIKE %s ORDER BY timestamp DESC",
        (f"{prefix}%",)
    )
    raw_msgs = cursor.fetchall()
    conn.commit()
    conn.close()

    filter_on = session.get("filter", True)
    msgs = []
    for msg in raw_msgs:
        content = blur_bad_words(msg[1]) if filter_on else msg[1]
        msgs.append((msg[0].split("@")[0], content, msg[2], msg[3]))

    return render_template("messages.html",
        email=email,
        address=address,
        messages=msgs,
        level_name=level_names[current_level],
        prefix=prefix,
        filter_on=filter_on
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
            "SELECT id, author_email, title, timestamp, origin_address, nsfw FROM library WHERE origin_address LIKE %s ORDER BY timestamp DESC",
        (f"{prefix}%",)
    )
    raw_entries = cursor.fetchall()
    conn.commit()
    conn.close()

    filter_on = session.get("filter", True)
    entries = []
    for e in raw_entries:
        auto_flag = contains_bad_words(e[2])
        is_nsfw = e[5] or auto_flag
        title = blur_bad_words(e[2]) if filter_on and is_nsfw else e[2]
        entries.append({
            "id": e[0],
            "author": e[1].split("@")[0],
            "title": title,
            "timestamp": e[3],
            "address": e[4],
            "nsfw": is_nsfw,
            "blocked": is_nsfw and filter_on
        })

    return render_template("library.html",
        email=email,
        address=address,
        entries=entries,
        level_name=level_names[current_level],
        prefix=prefix,
        filter_on=filter_on
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
        "SELECT author_email, title, content, timestamp, origin_address FROM library WHERE id = %s",
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
        nsfw = "nsfw" in request.form
        auto_flag = contains_bad_words(title) or contains_bad_words(content)
        is_nsfw = nsfw or auto_flag
        if title.strip() and content.strip():
            conn = get_connections()
            cursor = conn.cursor()
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            cursor.execute(
                "INSERT INTO library (origin_address, author_email, title, content, timestamp, nsfw) VALUES (%s, %s, %s, %s, %s, %s)",
                (address, email, title, content, timestamp, is_nsfw)
            )
            conn.commit()
            conn.close
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
        "SELECT current_level, travel_started, destination_level FROM travel WHERE email = %s",
        (email,)
    )
    status = cursor.fetchone()
    if not status:
        cursor.execute(
            "INSERT INTO travel (email, current_level, travel_started, destination_level) VALUES (%s, 3, NULL, NULL)",
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
                "UPDATE travel SET current_level = %s, travel_started = NULL, destination_level = NULL WHERE email = %s",
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
        """
        INSERT INTO travel (
             email,
             current_level,
             travel_started,
             destination_level
         )
         VALUES (%s, %s, %s, %s)
         ON CONFLICT (email)
         DO UPDATE SET
             current_level = EXCLUDED.current_level,
             travel_started = EXCLUDED.travel_started,
             destination_level = EXCLUDED.destination_level
         """,
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
        "SELECT current_level FROM travel WHERE email = %s", 
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
        "SELECT origin_address, author_email, content, timestamp FROM messages WHERE origin_address LIKE %s ORDER BY timestamp DESC LIMIT 30",
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

import random
from database import get_connections
from datetime import date

def generate_address(cursor):
    sub = random.randint(1, 9)
    city = random.randint(1, 20)
    districts = list(range(1, 21))
    random.shuffle(districts)


    for d in districts:
        address = f"#0-{sub}-{city:02d}-{d:04d}"
        cursor.execute(
            "SELECT COUNT(*) FROM members WHERE address = %s",
            (address,)
        )
        count = cursor.fetchone()[0]
        if count < 9999:
            return address
    return None

# i hate syntax..

def assign_member(email):
    conn = get_connections()
    cursor = conn.cursor()

    cursor.execute(
       "SELECT address FROM members WHERE email = %s",
       (email,)
    )
    existing = cursor.fetchone()


    if existing:
        conn.close()
        return


    adress = generate_address(cursor)


    if not adress:
        print("the wired is full.. somehow...")
        conn.close()
        return


    today = date.today().isoformat()
    cursor.execute(
        "INSERT INTO members (email, address, joined_date) VALUES (%s, %s, %s)",
        (email, adress, today)
    )

    conn.commit()
    conn.close()

    print(f"you have been assigned to district {adress}")


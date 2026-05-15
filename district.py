import json
import random
import os 

DATA_FILE = "districts.json"


# lock in..

def load_data(): 
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f: 
            return json.load(f)
    return {"districts": {}, "members": {}}


def save_data(data): 
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def generate_address(data):
    sub = random.randint(1, 9)
    city = random.randint(1, 20)
    district = random.randint(1, 20)

    districts = list(range(1, 21))
    random.shuffle(districts)
    for d in districts:
        adress = f"#0-{sub}-{city:02d}-{d:04d}"
        if adress not in data["districts"]:
            return adress
        if len(data["districts"][adress]["members"]) < 9999:
            return adress

    return None

def assign_member(email):
    data = load_data()

    if email in data["members"]:
        adress = data["members"][email]
        print(f"Welcome back, you are in {address}")
        return

    address = generate_address(data)

    if address not in data["districts"]:
        data["districts"][address] = {"members": []}

    data["districts"][address]["members"].append(email)
    data["members"][email] = address

    save_data(data)
    print(f"welcome to the wired, {email}")
    print(f"you have been assigened to district {address}")

email = input("enter you email: ")
assign_member(email)

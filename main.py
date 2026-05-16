from district import assign_member
from messages import post_message, read_message
from library import write_entry, read_library, read_entry
from database import get_connections

# alright, I have all the pecices.. now let's smash it out!

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


def main():
    print("\nwelcome to the wired")
    print("we are all connected\n")

    email = input("enter your email: ")

    member = get_member(email)
    address = member[0]

    print(f"\nyou are in district {address}")

    while True:
        print("\nwhat would you like to do?")
        print("1. read message board")
        print("2. post a message")
        print("3. read the library")
        print("4. write to the library")
        print("5. read a specific library entry")
        print("6. quit")

        choice = input("\n> ")

        if choice == "1":
            read_message(address)

        elif choice == "2":
            content = input("your message: ")
            post_message(email, address, content)

        elif choice == "3": 
            read_library(address)

        elif choice == "4":
            title = input("entry title: ")
            print("write your entry below, when it's done type END on a new line")
            lines = []
            while True:
                line = input()
                if line == "END":
                    break
                lines.append(line)
            content = "\n".join(lines)
            write_entry(email, address, title, content)

        elif choice == "5":
            title = input("entry title to read: ")
            read_entry(address, title)

        elif choice == "6" or choice =="q":
            print("\nsee you in the wired\n")
            break

        else:
            print("invalid choice, try again")

# praying sytax is right

main()


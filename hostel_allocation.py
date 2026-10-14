"""Hostel room allocation system with basic security and validation."""
import os
import secrets

import yaml
from flask import Flask, request
from markupsafe import escape


# Global hostel state.
rooms = {}
allocations = {}
waitlist = []
app = Flask(__name__)

CONFIG = """
blocks:
  A: {gender: M, rooms: 3, capacity: 2, fee: 4000}
  B: {gender: F, rooms: 2, capacity: 3, fee: 3500}
"""


def load_config(text=CONFIG):
    """Load hostel configuration safely and initialize the rooms."""
    config = yaml.safe_load(text)

    if not isinstance(config, dict) or not isinstance(
        config.get("blocks"), dict
    ):
        raise ValueError("Invalid hostel configuration.")

    rooms.clear()
    allocations.clear()
    waitlist.clear()

    for block, info in config["blocks"].items():
        for number in range(1, info["rooms"] + 1):
            room_number = f"{block}{number}"
            rooms[room_number] = {
                "gender": info["gender"],
                "capacity": info["capacity"],
                "fee": info["fee"],
                "occupants": [],
            }

    return config


def allocate_room(
    student_id, name, gender, year, preferred=None
):
    """Allocate an eligible room to a student."""
    if not isinstance(year, int) or isinstance(year, bool) or year < 1:
        return None

    if not all(isinstance(value, str) and value.strip() for value in (
        student_id, name, gender
    )):
        return None

    if student_id in allocations:
        return allocations[student_id]["room"]

    gender = gender.strip().upper()
    preferences = list(preferred) if preferred is not None else []
    candidates = preferences + [
        room_number
        for room_number in rooms
        if room_number not in preferences
    ]

    for room_number in candidates:
        room = rooms.get(room_number)

        if room is None:
            continue

        if room["gender"] != gender:
            continue

        if len(room["occupants"]) >= room["capacity"]:
            continue

        room["occupants"].append(student_id)
        allocations[student_id] = {
            "name": name.strip(),
            "room": room_number,
            "year": year,
        }

        if student_id in waitlist:
            waitlist.remove(student_id)

        return room_number

    if student_id not in waitlist:
        waitlist.append(student_id)

    return None


def vacate_room(student_id):
    """Remove a student from their room and allocation records."""
    allocation = allocations.pop(student_id, None)

    if allocation is None:
        return False

    room = rooms.get(allocation["room"])

    if room is not None and student_id in room["occupants"]:
        room["occupants"].remove(student_id)

    return True


def monthly_fee(student_id, days_stayed):
    """Calculate the fee using 30-day billing periods."""
    if (
        not isinstance(days_stayed, int)
        or isinstance(days_stayed, bool)
        or days_stayed < 0
    ):
        raise ValueError("Days stayed must be a non-negative integer.")

    allocation = allocations.get(student_id)

    if allocation is None:
        raise ValueError("Student has no room allocation.")

    room = rooms[allocation["room"]]
    months = (days_stayed + 29) // 30

    return months * room["fee"]


def priority_order(students):
    """Return students ordered from most senior to least senior."""
    return sorted(students, key=lambda student: student["year"], reverse=True)


def room_lottery(student_ids):
    """Return student IDs in a securely randomized order."""
    return secrets.SystemRandom().sample(
        list(student_ids), len(student_ids)
    )


def vacant_beds():
    """Count all unoccupied beds across the hostel."""
    return sum(
        room["capacity"] - len(room["occupants"])
        for room in rooms.values()
    )


def sqlite_connect(host, user, password):
    """Represent the connection status of the demonstration database."""
    return {
        "host": host,
        "user": user,
        "connected": bool(password),
    }


def connect_warden_db():
    """Read the demonstration database password from the environment."""
    password = os.getenv("WARDEN_DB_PASSWORD", "")

    return sqlite_connect(
        host="localhost",
        user="warden",
        password=password,
    )


@app.route("/room")
def room_lookup():
    """Display the room allocation for a student ID."""
    student_id = request.args.get("id", "")
    allocation = allocations.get(student_id)

    if allocation is None:
        return (
            f"<h1>No room allocation found for "
            f"{escape(student_id)}</h1>"
        ), 404

    room_number = allocation["room"]

    return (
        f"<h1>Room for {escape(student_id)}: "
        f"{escape(room_number)}</h1>"
    )


def run_portal():
    """Start the Flask portal with debug mode disabled."""
    app.run(debug=False)


def main():
    """Run the hostel allocation demonstration."""
    load_config()

    print("Rooms:", list(rooms.keys()))
    print("S1 ->", allocate_room("S1", "Arjun", "M", 1))
    print("S2 ->", allocate_room("S2", "Kabir", "M", 2))
    print("S3 ->", allocate_room("S3", "Rohan", "M", 3))
    print("S4 (female) ->", allocate_room("S4", "Diya", "F", 1))
    print("S1 again ->", allocate_room("S1", "Arjun", "M", 1))
    print("S5 year '2' ->", allocate_room("S5", "Vikram", "M", "2"))
    print("Occupants of A1:", rooms["A1"]["occupants"])

    vacate_room("S2")

    print("Occupants of A1 after S2 left:", rooms["A1"]["occupants"])
    print("Fee for S1, 45 days:", monthly_fee("S1", 45))

    students = [{"year": 1}, {"year": 4}, {"year": 2}]

    print(
        "Priority (seniors first?):",
        [student["year"] for student in priority_order(students)],
    )

    print("Lottery:", room_lottery(["S6", "S7", "S8"]))
    print("Vacant beds:", vacant_beds())
    print("Warden DB:", connect_warden_db())
    print("Waitlist:", waitlist)


if __name__ == "__main__":
    main()

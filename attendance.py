
import csv
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "attendance.csv"


def get_member_status(member_id):
    if not DATA_FILE.exists():
        return "checked_out"

    status = "checked_out"

    with open(DATA_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["member_id"] == str(member_id):
                status = row["action"]

    return status


def save_attendance(member_id, action):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    file_exists = DATA_FILE.exists()

    with open(DATA_FILE, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["member_id", "action", "timestamp"])

        writer.writerow([
            member_id,
            action,
            datetime.now().isoformat(timespec="seconds")
        ])


def check_in(member_id):
    if get_member_status(member_id) == "checked_in":
        raise ValueError("Member is already checked in.")

    save_attendance(member_id, "checked_in")
    print(f"Member {member_id} checked in successfully.")


def check_out(member_id):
    if get_member_status(member_id) != "checked_in":
        raise ValueError("Member is not checked in.")

    save_attendance(member_id, "checked_out")
    print(f"Member {member_id} checked out successfully.")


def get_current_occupancy():
    if not DATA_FILE.exists():
        return 0

    statuses = {}

    with open(DATA_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            statuses[row["member_id"]] = row["action"]

    return sum(
        status == "checked_in"
        for status in statuses.values()
    )


import csv
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "attendance.csv"


def validate_member_id(member_id):
    # Check the member ID before using it
    if isinstance(member_id, bool) or not isinstance(
        member_id, (str, int)
    ):
        raise ValueError("Invalid member ID.")

    member_id = str(member_id).strip()

    if not member_id:
        raise ValueError("Member ID cannot be empty.")

    return member_id


def read_attendance_records():
    if not DATA_FILE.exists():
        return []

    with open(DATA_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        required = {"member_id", "action", "timestamp"}

        if not reader.fieldnames or not required.issubset(
            reader.fieldnames
        ):
            raise ValueError("Invalid attendance CSV header.")

        records = []

        for row in reader:
            member_id = (row.get("member_id") or "").strip()
            action = row.get("action")
            timestamp = row.get("timestamp")

            if None in row or not member_id:
                raise ValueError("Invalid attendance record.")

            if action not in ("checked_in", "checked_out"):
                raise ValueError("Invalid attendance action.")

            try:
                datetime.fromisoformat(timestamp)
            except (ValueError, TypeError):
                raise ValueError("Invalid attendance timestamp.")

            records.append(row)

        return records


def get_member_status(member_id):
    member_id = validate_member_id(member_id)
    status = "checked_out"

    for row in read_attendance_records():
        if row["member_id"] == member_id:
            status = row["action"]

    return status


def save_attendance(member_id, action):
    member_id = validate_member_id(member_id)

    if action not in ("checked_in", "checked_out"):
        raise ValueError("Invalid attendance action.")

    # Validate existing records before writing
    read_attendance_records()

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    file_exists = DATA_FILE.exists()

    with open(DATA_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["member_id", "action", "timestamp"])

        writer.writerow([
            member_id,
            action,
            datetime.now().isoformat(timespec="seconds")
        ])


def check_in(member_id):
    member_id = validate_member_id(member_id)

    if get_member_status(member_id) == "checked_in":
        raise ValueError("Member is already checked in.")

    save_attendance(member_id, "checked_in")
    print(f"Member {member_id} checked in successfully.")


def check_out(member_id):
    member_id = validate_member_id(member_id)

    if get_member_status(member_id) != "checked_in":
        raise ValueError("Member is not checked in.")

    save_attendance(member_id, "checked_out")
    print(f"Member {member_id} checked out successfully.")


def get_current_occupancy():
    statuses = {}

    for row in read_attendance_records():
        statuses[row["member_id"]] = row["action"]

    return sum(
        status == "checked_in"
        for status in statuses.values()
    )

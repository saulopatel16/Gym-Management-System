import pandas as pd
import attendance

def get_attendance_summary():
    # Default summary when no data exists
    summary = {
        "total_checkins": 0,
        "total_checkouts": 0,
        "unique_members": 0,
        "current_occupancy": 0,
        "daily_checkins": {}
    }

    # Check if attendance records exist
    records = attendance.read_attendance_records()

    if not records:
        return summary

    df = pd.DataFrame(records)


    # Convert timestamps to datetime objects
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Separate check-ins and check-outs
    checkins = df[df["action"] == "checked_in"]
    checkouts = df[df["action"] == "checked_out"]

    # Count check-ins for each day
    daily = checkins.groupby(
        checkins["timestamp"].dt.strftime("%Y-%m-%d")
    ).size()

    # Calculate attendance statistics
    summary["total_checkins"] = len(checkins)
    summary["total_checkouts"] = len(checkouts)
    summary["unique_members"] = checkins["member_id"].nunique()
    summary["current_occupancy"] = attendance.get_current_occupancy()

    summary["daily_checkins"] = {
        date: int(count)
        for date, count in daily.items()
    }

    return summary


if __name__ == "__main__":
    summary = get_attendance_summary()

    print("=== Gym Attendance Summary ===")
    print("Total Check-ins:", summary["total_checkins"])
    print("Total Check-outs:", summary["total_checkouts"])
    print("Unique Members:", summary["unique_members"])
    print("Current Occupancy:", summary["current_occupancy"])

    print("\n=== Daily Check-ins ===")
    for date, count in summary["daily_checkins"].items():
        print(f"{date}: {count}")

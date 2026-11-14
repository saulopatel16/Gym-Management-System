
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from attendance_analysis import get_attendance_summary


def create_daily_attendance_chart(output_path="charts/daily_attendance.png"):
    # Get attendance statistics
    summary = get_attendance_summary()
    daily_checkins = summary["daily_checkins"]

    # Check if attendance records exist
    if not daily_checkins:
        print("No attendance data available for visualization.")
        return None

    # Prepare data for the chart
    dates = sorted(daily_checkins.keys())
    counts = [daily_checkins[date] for date in dates]

    # Create the bar chart
    fig, ax = plt.subplots(figsize=(10, 6))

    bars = ax.bar(dates, counts, color="steelblue")

    # Add chart title and labels
    ax.set_title("Daily Gym Attendance")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Check-ins")

    # Display check-in numbers on bars
    ax.bar_label(bars, padding=3)

    # Format the chart
    ax.set_ylim(0, max(counts) + 1)
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()

    # Save chart as a PNG file
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig.savefig(output_path)
    plt.close(fig)

    print(f"Attendance chart saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    create_daily_attendance_chart()

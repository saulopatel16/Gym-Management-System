
import pytest
import attendance
from attendance_analysis import get_attendance_summary


@pytest.fixture
def setup_data(tmp_path, monkeypatch):
    # Use a temporary CSV file for each test
    test_file = tmp_path / "attendance.csv"
    monkeypatch.setattr(attendance, "DATA_FILE", test_file)
    return test_file


def test_no_attendance_records(setup_data):
    summary = get_attendance_summary()

    assert summary["total_checkins"] == 0
    assert summary["total_checkouts"] == 0
    assert summary["current_occupancy"] == 0
    assert summary["daily_checkins"] == {}


def test_single_member_attendance(setup_data):
    attendance.check_in("M001")
    attendance.check_out("M001")

    summary = get_attendance_summary()

    assert summary["total_checkins"] == 1
    assert summary["total_checkouts"] == 1
    assert summary["unique_members"] == 1
    assert summary["current_occupancy"] == 0


def test_multiple_members(setup_data):
    attendance.check_in("M001")
    attendance.check_in("M002")
    attendance.check_in("M003")

    summary = get_attendance_summary()

    assert summary["total_checkins"] == 3
    assert summary["unique_members"] == 3
    assert summary["current_occupancy"] == 3


def test_daily_attendance(setup_data):
    # Create records covering two different days
    setup_data.write_text(
        "member_id,action,timestamp\n"
        "M001,checked_in,2026-11-13T09:00:00\n"
        "M001,checked_out,2026-11-13T10:00:00\n"
        "M002,checked_in,2026-11-13T11:00:00\n"
        "M001,checked_in,2026-11-14T09:00:00\n"
    )

    summary = get_attendance_summary()

    assert summary["total_checkins"] == 3
    assert summary["unique_members"] == 2
    assert summary["daily_checkins"] == {
        "2026-11-13": 2,
        "2026-11-14": 1
    }

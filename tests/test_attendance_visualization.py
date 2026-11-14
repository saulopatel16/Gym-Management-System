
import pytest
import attendance
from attendance_visualization import create_daily_attendance_chart


@pytest.fixture
def setup_data(tmp_path, monkeypatch):
    # Use temporary attendance data
    test_file = tmp_path / "attendance.csv"
    monkeypatch.setattr(attendance, "DATA_FILE", test_file)
    return tmp_path


def test_no_attendance_data(setup_data):
    output = setup_data / "empty_chart.png"

    result = create_daily_attendance_chart(output)

    assert result is None
    assert not output.exists()


def test_create_chart(setup_data):
    attendance.check_in("M001")

    output = setup_data / "daily_chart.png"
    result = create_daily_attendance_chart(output)

    assert result == output
    assert output.exists()
    assert output.stat().st_size > 0


def test_multiple_days_chart(setup_data):
    # Create sample attendance records
    attendance.DATA_FILE.write_text(
        "member_id,action,timestamp\n"
        "M001,checked_in,2026-11-13T09:00:00\n"
        "M002,checked_in,2026-11-13T10:00:00\n"
        "M003,checked_in,2026-11-14T09:00:00\n"
    )

    output = setup_data / "multiple_days.png"
    result = create_daily_attendance_chart(output)

    assert result == output
    assert output.exists()
    assert output.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")

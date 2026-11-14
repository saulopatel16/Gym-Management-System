
import pytest
import attendance


@pytest.fixture
def setup_data(tmp_path, monkeypatch):
    test_file = tmp_path / "attendance.csv"
    monkeypatch.setattr(attendance, "DATA_FILE", test_file)
    return test_file


def test_empty_member_id(setup_data):
    with pytest.raises(ValueError, match="cannot be empty"):
        attendance.check_in("   ")


def test_invalid_member_id_type(setup_data):
    with pytest.raises(ValueError, match="Invalid member ID"):
        attendance.check_in(None)


def test_member_id_with_spaces(setup_data):
    attendance.check_in("  M001  ")

    assert attendance.get_member_status("M001") == "checked_in"
    assert attendance.get_current_occupancy() == 1

    attendance.check_out(" M001 ")

    assert attendance.get_current_occupancy() == 0


def test_invalid_csv_header(setup_data):
    setup_data.write_text(
        "member,action,timestamp\n"
        "M001,checked_in,2026-11-14T09:00:00\n"
    )

    with pytest.raises(ValueError, match="CSV header"):
        attendance.read_attendance_records()


def test_invalid_attendance_action(setup_data):
    setup_data.write_text(
        "member_id,action,timestamp\n"
        "M001,unknown,2026-11-14T09:00:00\n"
    )

    with pytest.raises(ValueError, match="Invalid attendance action"):
        attendance.get_current_occupancy()


def test_invalid_timestamp(setup_data):
    setup_data.write_text(
        "member_id,action,timestamp\n"
        "M001,checked_in,invalid-date\n"
    )

    with pytest.raises(ValueError, match="Invalid attendance timestamp"):
        attendance.read_attendance_records()


def test_corrupted_csv_not_overwritten(setup_data):
    original_data = (
        "member_id,action,timestamp\n"
        "M001,invalid_action,2026-11-14T09:00:00\n"
    )

    setup_data.write_text(original_data)

    with pytest.raises(ValueError):
        attendance.check_in("M002")

    assert setup_data.read_text() == original_data

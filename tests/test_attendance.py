
import pytest
import attendance


@pytest.fixture
def setup_attendance(tmp_path, monkeypatch):
    test_file = tmp_path / "attendance.csv"
    monkeypatch.setattr(attendance, "DATA_FILE", test_file)


def test_check_in(setup_attendance):
    attendance.check_in("M001")

    assert attendance.get_member_status("M001") == "checked_in"
    assert attendance.get_current_occupancy() == 1


def test_check_out(setup_attendance):
    attendance.check_in("M001")
    attendance.check_out("M001")

    assert attendance.get_member_status("M001") == "checked_out"
    assert attendance.get_current_occupancy() == 0


def test_duplicate_check_in(setup_attendance):
    attendance.check_in("M001")

    with pytest.raises(ValueError):
        attendance.check_in("M001")


def test_check_out_without_check_in(setup_attendance):
    with pytest.raises(ValueError):
        attendance.check_out("M001")


def test_multiple_members(setup_attendance):
    attendance.check_in("M001")
    attendance.check_in("M002")
    attendance.check_in("M003")

    assert attendance.get_current_occupancy() == 3

    attendance.check_out("M002")

    assert attendance.get_current_occupancy() == 2

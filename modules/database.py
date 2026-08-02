import csv
from pathlib import Path

DB_PATH = Path("database/visitors.csv")
HEADERS = ["first_name", "surname", "full_name", "visit_timestamp", "photo_uploaded", "video_filename"]


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not DB_PATH.exists():
        with open(DB_PATH, "w", newline="", encoding="utf-8") as file_handle:
            writer = csv.writer(file_handle)
            writer.writerow(HEADERS)


def _read_all():
    if not DB_PATH.exists():
        return []
    with open(DB_PATH, "r", newline="", encoding="utf-8") as file_handle:
        reader = csv.DictReader(file_handle)
        return list(reader)


def _write_all(rows):
    with open(DB_PATH, "w", newline="", encoding="utf-8") as file_handle:
        writer = csv.DictWriter(file_handle, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def check_visitor(first_name, surname):
    rows = _read_all()
    for row in rows:
        if row["first_name"].strip().lower() == first_name.strip().lower() and row["surname"].strip().lower() == surname.strip().lower():
            return True, row
    return False, None


def save_visitor(first_name, surname, full_name, timestamp, photo_uploaded, video_filename):
    rows = _read_all()
    rows.append(
        {
            "first_name": first_name,
            "surname": surname,
            "full_name": full_name,
            "visit_timestamp": timestamp,
            "photo_uploaded": str(photo_uploaded),
            "video_filename": video_filename,
        }
    )
    _write_all(rows)


def update_visitor_video(first_name, surname, video_filename):
    rows = _read_all()
    for row in rows:
        if row["first_name"].strip().lower() == first_name.strip().lower() and row["surname"].strip().lower() == surname.strip().lower():
            row["video_filename"] = video_filename
            row["photo_uploaded"] = "True"
            break
    _write_all(rows)

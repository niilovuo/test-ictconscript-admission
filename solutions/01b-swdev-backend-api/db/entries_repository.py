
import os
import sqlite3
from datetime import datetime

DB_PATH = os.path.join("db", "sqlite", "entries.db")
TABLE_NAME = "entries"

def get(id: int):
    db = connect_to_db()
    rows = db.execute(f"SELECT * FROM {TABLE_NAME} WHERE id = {id} ").fetchall()
    data = [dict(r) for r in rows]
    if len(data) == 0:
        raise ValueError(f"Could not find a record with id {id}")
    return data

def list():
    db = connect_to_db()
    rows = db.execute(f"SELECT * FROM {TABLE_NAME} ORDER BY isoTime desc").fetchall()
    data = [dict(r) for r in rows]
    return data

def create(title: str, body: str, lat: float = None, lon: float = None):
    db = connect_to_db()
    next_id = db.execute(f"SELECT COALESCE(MAX(CAST(id as INTEGER)), 0) + 1 FROM {TABLE_NAME}").fetchone()[0]
    timestamp = str(datetime.utcnow().isoformat(timespec="seconds") + "Z")

    db.execute(
        "INSERT INTO entries (id, title, body, isoTime, lat, lon) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (next_id, title, body, timestamp, lat, lon)
    )
    db.commit()
    return next_id, timestamp

def connect_to_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db
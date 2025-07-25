from flask import Flask, Response, jsonify, request
from db import entries_repository as repo

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health_check():
    return "OK", 200

@app.route("/entries", methods=["POST"])
def create_entry():
    entry_to_insert = request.get_json()
    try:
        try:
            lat, lon = entry_to_insert.get("lat"), entry_to_insert.get("lon")
            lat = float(lat) if lat is not None else None
            lon = float(lon) if lon is not None else None
        except ValueError:
            return "One or more coordinate parameters is not a number, please correct it and try again", 400
        id, timestamp = repo.create(
            title=entry_to_insert["title"],
            body=entry_to_insert["body"],
            lat=lat,
            lon=lon
        )
        return f"Successfully inserted entry {entry_to_insert} with id #{id} at {timestamp}", 200
    except KeyError as e:
        return f'Missing required parameter "{e.args[0]}"', 400

@app.route("/entries", methods=["GET"])
def list_entries():
    data = repo.list()
    return jsonify(data), 200

@app.route("/entries/<int:id>", methods=["GET"])
def get_entry(id: int):
    try:
        data = repo.get(id)
    except ValueError:
        return f"Entry #{id} not found", 404
    else:
        return jsonify(data), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
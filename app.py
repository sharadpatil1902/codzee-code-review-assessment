from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Complete Codzee assessment", "completed": False},
    {"id": 2, "title": "Review pull requests", "completed": False},
]


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/tasks")
def get_tasks():
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
    except (TypeError, ValueError):
        return jsonify({"error": "page and limit must be integers"}), 400

    if page < 1 or limit < 1 or limit > 100:
        return jsonify({
            "error": "page must be >= 1 and limit must be between 1 and 100"
        }), 400

    total = len(tasks)
    start = (page - 1) * limit

    return jsonify({
        "items": tasks[start:start + limit],
        "page": page,
        "limit": limit,
        "total": total,
        "pages": (total + limit - 1) // limit,
    })

@app.post("/tasks")
def create_task():
    data = request.get_json(silent=True) or {}

    task = {
        "id": max((item["id"] for item in tasks), default=0) + 1,
        "title": data.get("title"),
        "completed": False,
    }

    tasks.append(task)
    return jsonify(task), 201


if __name__ == "__main__":
    app.run(debug=True)
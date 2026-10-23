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
    return jsonify(tasks)


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
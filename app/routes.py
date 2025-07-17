from flask import Blueprint, request, jsonify
from .models import Task
from . import db

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    """API health check."""
    return jsonify({"status": "API is working"})


@main.route('/tasks', methods=['GET'])
def get_tasks():
    """Retrieve all tasks as a JSON list."""
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])


@main.route('/tasks', methods=['POST'])
def add_task():
    """Add a new task. Expects JSON: {'title': <str>}."""

    # Debugging output
    print("📥 Content-Type:", request.content_type)
    print("📥 Raw Body:", request.data)

    # Check Content-Type
    if not request.is_json:
        return jsonify({'message': 'Request must be application/json'}), 415

    # Try parsing JSON
    data = request.get_json(silent=True)
    if not data or 'title' not in data:
        return jsonify({'message': 'Title is required'}), 400

    # Add task
    new_task = Task(title=data['title'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201


@main.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    """Delete a task by ID."""
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'})

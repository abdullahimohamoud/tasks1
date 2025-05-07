from flask import Flask, request, jsonify
import json
import os
from uuid import uuid4

app = Flask(__name__)
TASKS_FILE = 'tasks.json'

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = load_tasks()
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    tasks = load_tasks()
    data = request.json
    new_task = {
        'id': str(uuid4()),
        'text': data.get('text', ''),
        'completed': data.get('completed', False),
        'priority': data.get('priority', 'medium'),
        'dueDate': data.get('dueDate'),
        'category': data.get('category', ''),
        'createdAt': data.get('createdAt')
    }
    tasks.insert(0, new_task)
    save_tasks(tasks)
    return jsonify(new_task), 201

@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    tasks = load_tasks()
    data = request.json
    for task in tasks:
        if task['id'] == task_id:
            task.update(data)
            save_tasks(tasks)
            return jsonify(task)
    return jsonify({'error': 'Task not found'}), 404

@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t['id'] != task_id]
    if len(new_tasks) == len(tasks):
        return jsonify({'error': 'Task not found'}), 404
    save_tasks(new_tasks)
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)

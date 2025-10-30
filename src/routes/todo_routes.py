from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from src.models import db, ToDo

todo_bp = Blueprint('todo_bp', __name__)

@todo_bp.route('/todo')
@login_required
def todo_list():
    todos = ToDo.query.filter_by(user_id=current_user.id).all()
    return render_template('todo.html', todos=todos)

@todo_bp.route('/todo/add', methods=['POST'])
@login_required
def add_todo():
    task = request.form.get('task')
    if task:
        new_task = ToDo(task=task, user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('todo_bp.todo_list'))

@todo_bp.route('/todo/complete/<int:todo_id>')
@login_required
def complete_task(todo_id):
    task = ToDo.query.get_or_404(todo_id)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for('todo_bp.todo_list'))
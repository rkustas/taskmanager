from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.main.forms import AddTaskForm, SearchForm, DeleteTaskForm
from app.models import User, Task
from app.main import bp
from flask import g




@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    tasks = Task.query.all()
    return render_template('index.html', title='Tasks', tasks=tasks)

@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.index'))
    tasks = Task.search(g.search_form.q.data)
    print(tasks)
    return render_template('search.html', title='Search', tasks=tasks)

@bp.route('/delete/<int:task_id>', methods=['GET', 'POST'])
@login_required
def delete(task_id):
    task = Task.query.get(task_id)
    form = DeleteTaskForm()

    if task:
        if form.validate_on_submit():
            db.session.delete(task)
            db.session.commit()
            flash('Task has been deleted')
            return redirect(url_for('main.index'))

        return render_template('delete.html', form=form, task_id= task_id, title = task.title)
    else:
        flash('Task not found')

    return redirect(url_for('main.index'))

@bp.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit(task_id):
    task = Task.query.get(task_id)
    # print(task)
    form = AddTaskForm()

    if task:
        if form.validate_on_submit():
            task.title = form.title.data
            task.date = datetime.utcnow()
            db.session.commit()
            flash('Task has been updated')
            return redirect(url_for('main.index'))

        form.title.data = task.title
        return render_template('edit.html', form=form, title="Edit Task",task_id= task_id)
    else:
        flash('Task not found')

    return redirect(url_for('main.index'))

@bp.route('/mytasks/<username>',methods=['GET','POST'])
@login_required
def mytasks(username):
    user = User.query.filter_by(username=username).first_or_404()
    tasks = user.tasks.order_by(Task.date.desc())
    return render_template('mytasks.html', user=user,tasks=tasks, title='My Tasks')

@bp.route('/add/<username>', methods=['GET','POST'])
@login_required
def add(username):
    form = AddTaskForm()
    if form.validate_on_submit():
        t = Task(title=form.title.data, date=datetime.utcnow(), user=current_user, duedate=form.dt.data)
        db.session.add(t)
        db.session.commit()
        flash('Task added to the database')
        return redirect(url_for('main.index'))
    return render_template('add.html', form=form, title='Add Task')

@bp.route('/newtasks')
@login_required
def newtasks():
    tasks = current_user.new_tasks()
    if tasks:
        current_user.last_task_read_time = datetime.utcnow()
        db.session.commit()
        return render_template('newtasks.html', title="New Tasks", tasks=tasks)
    return redirect(url_for('main.index'))
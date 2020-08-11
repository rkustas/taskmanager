from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.main.forms import AddTaskForm, SearchForm, DeleteTaskForm
from app.models import User, Task
from app.main import bp
from flask import g
from app.emailpy import task_update, pastdue_email




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
    page = request.args.get('page', 1, type=int)
    tasks = Task.query.order_by(Task.date.desc()).paginate(page,current_app.config['POSTS_PER_PAGE'],False)
    next_url = url_for('main.index', page=tasks.next_num) \
        if tasks.has_next else None
    prev_url = url_for('main.index', page=tasks.prev_num) \
        if tasks.has_prev else None
    return render_template('index.html', title='Tasks', tasks=tasks.items, next_url=next_url, prev_url=prev_url)

@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    tasks, total = Task.search(g.search_form.q.data, page, current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title='Search', tasks=tasks,next_url=next_url,prev_url=prev_url)

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
            task.duedate = form.dt.data
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
    page = request.args.get('page', 1, type=int)
    tasks = user.tasks.order_by(Task.date.desc()).paginate(page,current_app.config['POSTS_PER_PAGE'],False)
    next_url = url_for('main.mytasks', username=user.username, page=tasks.next_num) \
        if tasks.has_next else None
    prev_url = url_for('main.mytasks', username=user.username, page=tasks.prev_num) \
        if tasks.has_prev else None
    return render_template('mytasks.html', user=user,tasks=tasks.items, title='My Tasks',next_url=next_url,prev_url=prev_url)

@bp.route('/add/<username>', methods=['GET','POST'])
@login_required
def add(username):
    users = User.query.all()
    form = AddTaskForm()
    if form.validate_on_submit():
        t = Task(title=form.title.data, date=datetime.utcnow(), user=current_user, duedate=form.dt.data)
        db.session.add(t)
        db.session.commit()
        for user in users:
            task_update(user)
        flash('Task added to the database')
        return redirect(url_for('main.index'))
    return render_template('add.html', form=form, title='Add Task', users=users)

@bp.route('/newtasks')
@login_required
def newtasks():
    tasks = current_user.new_tasks()
    if tasks:
        current_user.last_task_read_time = datetime.utcnow()
        db.session.commit()
        return render_template('newtasks.html', title="New Tasks", tasks=tasks)
    flash('0 new tasks')
    return render_template('newtasks.html', title="New Tasks", tasks=tasks)

@bp.route('/pastdue')
def pastdue():
    pastduetasks = Task.query.filter(Task.duedate < Task.date).all()
    for p in pastduetasks:
        pastdue_email(p)
        return jsonify([{
            'name': p.user.username,
            'title': p.title,
            'email': p.user.email
        } for p in pastduetasks])
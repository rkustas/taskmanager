from app import app, db
from flask import render_template, redirect, url_for, flash, get_flashed_messages
from models import Task
from datetime import datetime

import forms

# Basic route
@app.route('/')
@app.route('/index')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET','POST'])
def add():
    form = forms.AddTaskForm()
    if form.validate_on_submit():
        t = Task(title=form.title.data, date=datetime.utcnow())
        db.session.add(t)
        db.session.commit()
        flash('Task added to the database')
        print('Submitted title', form.title.data)
        return redirect(url_for('index'))
    return render_template('add.html', form=form)
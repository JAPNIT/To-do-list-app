import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

""" Rather than registering views and other code directly with an
application, they are registered with a blueprint. Then the blueprint
is registered with the application when it is available in the factory
function. """

bp = Blueprint('task', __name__, url_prefix='/')

@bp.route('/', methods = ('GET','POST'))
def task():
	db = get_db()
	if request.method == 'POST':
		task_entered = request.form['task']
		db.execute('INSERT INTO task (description) VALUES (?)', (task_entered,))
		db.commit()

	checked = request.form.get('checked')
	print(checked)

	try:
		cur = db.cursor()
		cur.execute('SELECT * FROM task WHERE deleted_flag = 0')
		
		all_tasks = cur.fetchall()
		#try second method by using fetchall directly 
		
	except:
		all_tasks = ""

	return render_template('index.html', all_tasks = all_tasks)

def delete_task(task_id):
	db = get_db()
	try:
		db.execute('UPDATE task SET deleted_flag = 1 WHERE id = task_id')
		db.commit()

		cur = db.cursor()
		cur.execute('SELECT * FROM task WHERE deleted_flag = 0')
	        
		all_tasks = cur.fetchall()
	except:
		all_tasks = ""

	return render_template('index.html', all_tasks = all_tasks)




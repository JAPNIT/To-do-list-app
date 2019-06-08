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

		if len(task_entered) > 0:
			db.execute('INSERT INTO task (description) VALUES (?)', (task_entered,))
			db.commit()

		to_do = list(request.form.getlist('check'))
		print(to_do)
		print(request.form)

		for i in to_do:
			db.execute('UPDATE task SET deleted_flag = 1 WHERE id = i')
			db.commit()
		
			

	try:
		cur = db.cursor()
		cur.execute('SELECT * FROM task WHERE deleted_flag = 0')
		
		all_tasks = cur.fetchall()
		#try second method by using fetchall directly 
		
	except:
		all_tasks = ""

	return render_template('index.html', all_tasks = all_tasks)





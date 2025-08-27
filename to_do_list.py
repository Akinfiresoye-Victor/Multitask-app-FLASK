from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from wtforms.widgets import TextArea
from flask_wtf.file import FileField
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from datetime import datetime
from classes import ToDoList
import json
from databases import db,ToDO
from api_keys import api_key_currency, api_key_weather



app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///task.db'
app.config['SECRET_KEY']="legend"
db=SQLAlchemy(app)



@app.route('/todo', methods=['GET', 'POST'])
def schedules():
    form= ToDoList()
    todolist = ToDO.query.filter_by(user_id=current_user.id).order_by(ToDO.date).all()
    task=None
    date=None
    flash('Plan your chores with our quality Schedule app📓')
    if form.validate_on_submit():
        try:
            task=form.task.data
            date=form.date.data
            if date == '':
                date='Anytime'
            db.session.add(ToDO(task=task, date=date, user_id=current_user.id))  
            #committing what we've added
            db.session.commit()
            form.task.data= ''
            form.date.data=''
            todolist = ToDO.query.filter_by(user_id=current_user.id).order_by(ToDO.date).all()
            flash('Task created, youre ready to go🚀')
            return redirect(url_for('schedules'))
        except:
            flash('Oops... seems there was an error please try again😥')    
    
    return render_template('schedule.html', form=form, task=task, date=date, todolist=todolist)


if __name__ =='__main__':
    with app.app_context():
            app.run(debug=True)
    
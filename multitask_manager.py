#importing modules


from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from wtforms.widgets import TextArea
from flask_wtf.file import FileField
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash  #this is used to hash passwords
import requests
from datetime import datetime
from classes import ToDoList, PasswordForm, RegistrationForm, LoginForm, PasswordManager, Enter, Weather, Currency, UpdateForm,Bible
import json
from databases import app, db, User, ToDO, Password
from api_keys import api_key_currency, api_key_weather



#database initiation


#migration stuff
migrate= Migrate(app, db)

#login mechanism
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'


#password handling routes
@property
def password(self):
    raise AttributeError('password is not a readable attribute')
@password.setter
def password(self, password):
    self.password_hash= generate_password_hash(password)
def verify_password(self, password):
    return check_password_hash(self.password_hash, password)
@login_manager.user_loader
def load_users(user_id):
    #User.query.get(int(user_id))-> this has been depreciated
    return db.session.get(User, user_id)
    #db.session.execute(db.select(User).filter_by(id=1)).scalar()-> this can also be used if we want to filter 
        
#homepage    
@app.route('/')
def homepage():
    if current_user.is_authenticated:
            flash('You are already logged in, you can now explore😁')
            flash('And sorry i am lazy no time to place emojis everywhere😅')
    else:        
        flash('Hey there Get started/login to have unrestricted access')

    return render_template('homepage.html')


#function for registering users
@app.route('/register', methods=['GET', 'POST'])    
def register():
    flash('Fill all boxes')
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_pw=generate_password_hash(form.password.data, "pbkdf2:sha256")
        user= User.query.filter_by(username=form.username.data).first()
        user2= User.query.filter_by(name=form.name.data).first()
        if user and user2: 
            registered_user=User.query.order_by(User.date).all() 
            flash('User already exists, change your name or username(^_^)')
            return render_template('register.html', form=form, name=form.name.data, username=form.username.data, registered_user=registered_user, key_word=form.key_word.data) 
        elif user is None and user2 is None: 
            try:
                db.session.add(User(name=form.name.data, username=form.username.data, password_hash=hashed_pw,key_word=form.key_word.data))
                db.session.commit()
                flash('Registered successful')
                return redirect(url_for('login'))
            except:
                flash('An issue occurred crosscheck and try again.....')
            
        form.name.data=''
        form.username.data=''
        form.password.data=''
        form.password2.data=''   
        form.key_word.data=''         
    elif form.password.data != form.password2.data:
        flash("Password dosen't mach")
    registered_user=User.query.order_by(User.date).all()     
    return render_template('register.html', form=form, name=form.name.data, username=form.username.data,registered_user=registered_user, key_word=form.key_word.data)        


#function for login in user
@app.route('/login', methods=['GET', 'POST'])
def login():
    form= LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username= form.username.data).first()
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                return redirect(url_for('homepage'))
            else:
                flash('Password Incorrect')
                return redirect(url_for('login'))
        else:
            flash('User not found')
            return redirect (url_for('login'))
    return render_template('login.html', form=form) 

#logout function
@app.route('/logout', methods=['GET', 'POST'] )
@login_required
def logout():
    logout_user()
    flash('You have been logged out thanks for stopping by')
    return redirect(url_for('homepage'))               

#current updates    
@app.route('/updates', methods=['GET', 'POST'])  
@login_required
def updates():
    form = Currency()
    currency1 = form.currency1.data
    currency2 = form.currency2.data
    currency3 = form.currency3.data
    currency4 = form.currency4.data
    data_json = None
    if form.validate_on_submit():
        if all(len(currency) == 3 for currency in [currency1, currency2, currency3, currency4] if currency):  # Check valid length
            try:
                import http.client
                conn = http.client.HTTPSConnection("api.currencyfreaks.com")
                payload = ''
                headers = {}
                conn.request("GET", f"/v2.0/rates/latest?base=usd&symbols={currency1},{currency2},{currency3},{currency4}&apikey={api_key_currency}", payload, headers)
                res = conn.getresponse()
                data = res.read()
                data_str = data.decode("utf-8")
                data_json = json.loads(data_str)
                return render_template('updates.html', form=form, currency1=currency1, currency2=currency2, currency3=currency3, currency4=currency4, data_json=data_json)
            
            except:
                flash('An error occurred while fetching data. Please try again.')
        else:
            flash('Each keyword should be 3 letters.')


    flash(f"Welcome back {current_user.username}")
    return render_template('updates.html', form=form, currency1=currency1, currency2=currency2, currency3=currency3, currency4=currency4, data_json=data_json)
 
#function for updating users    
@app.route('/update/<int:id>', methods=['GET', 'POST'])   
@login_required 
def update(id):
    form=UpdateForm()
    id=current_user.id
    update= User.query.get(id)
    form.name.data=current_user.name
    form.username.data=current_user.username
    form.key_word.data=current_user.key_word


    if request.method=="POST":
        update.name=request.form['name']
        update.username=request.form['username']
        update.key_word=request.form['key_word']
        
        try:
            db.session.commit()
            form.name.data=current_user.name
            form.username.data=current_user.username
            form.key_word.data=current_user.key_word
            flash('Profile Updated')
        except:
            flash('An error occurred while updating profile')    
    return render_template('update.html', form=form, id=id, update=update)    
                  
#function for updating users password         
@app.route('/passupd/<int:id>', methods=['GET', 'POST'])                
@login_required
def update_password(id):  
    form=UpdateForm()      
    id=current_user.id
    update= User.query.get(id)

    if request.method=="POST":
        if check_password_hash(current_user.password_hash, form.password_scan.data):
            
            update.password_hash=generate_password_hash(form.password.data)
            try:
                db.session.commit()
                flash('Password Updated successfully!!')
                return redirect(url_for('update'))
            except:
                    flash('An error occurred while updating password')   
        else:
            flash('Incorrect password')                     
    return render_template('update_password.html', form=form, id=id, update=update) 
    
    
    
    
    
    
#function authenticating user before getting to the password  manager
@app.route('/password', methods=['GET', 'POST'])
@login_required
def password_manager_gate():
    form=PasswordManager()
    if form.validate_on_submit():
        key_word=form.key_word.data
        user=User.query.filter_by(username=current_user.username).first()
        passwords = Password.query.filter_by(user_id = current_user.id).all()
        if user:
            if check_password_hash(user.password_hash, form.password.data) and user.key_word==form.key_word.data:
                flash(f"Hey {current_user.username} fear not your passwords are kept safe with us😆, wanna add more?😊" )
                return redirect(url_for('password_manager'))
            else:
                flash('Incorrect Password or key Word please try again....')
                return render_template('password.html',key_word=key_word, username=current_user.username, form=form)
        else:
            flash('Are you sure u registered😑 if yes try again...😅')                                  
    return render_template('password.html', form=form)

#function for password manager
@app.route('/password/login', methods=['GET', 'POST'])
@login_required
def password_manager():
    form= Enter()
    passwords = Password.query.filter_by(user_id=current_user.id).order_by(Password.date).all()
    if form.validate_on_submit():
        try:
            site=form.site.data
            password=form.password.data
            password2=form.password2.data
            db.session.add(Password(site=site, password=password, user_id=current_user.id))
            db.session.commit()
            form.site.data=''
            form.password.data=''
            form.password2.data=''
            passwords = Password.query.filter_by(user_id=current_user.id).order_by(Password.date).all()
            flash('password Saved successfully✅')
            return redirect(url_for('password_manager'))
            
        except:
            flash('Please ensure the password is the same😐')
            return redirect(url_for('password_manager'))
    elif form.password.data != form.password2.data:
        flash('Password has to match...duhh🙄')        
    return render_template('password2.html', form=form, passwords=passwords)

#function for deleting passwords in saved passwords
@app.route('/delete/password/<int:id>')
def delete_password(id):
    try:
        pasd=Password.query.get(id)
        db.session.delete(pasd)
        db.session.commit()
        flash('Password deleted')
        return redirect(url_for('password_manager'))
    except:
        flash('Error deleting password')
        return redirect(url_for('password_manager'))  

#weather app
@app.route('/weather', methods=['GET', 'POST'])
def weather():
    form = Weather()
    if form.validate_on_submit():
        
        try:
            api_call = f'http://api.weatherstack.com/current?access_key={api_key_weather}&query={form.city.data}'
            weather_data=requests.get(api_call).json()['current']
            my_weather=f"Temperature is {weather_data['temperature']}°C, Humidity is {weather_data['humidity']}%, Pressure is {weather_data['pressure']} hpa"  
            city2=form.city.data    
            return render_template('weather.html', my_weather=my_weather, city2=city2, form=form)
        except:
            flash('Please enter a valid city name...🙂')
    return render_template('weather.html', form=form)
     
#bible app
@app.route('/bible', methods=['GET', 'POST'])

def bible():
    form=Bible()
    book=form.book.data
    chapter=form.chapter.data
    verse=form.verse.data
    flash('Sorry for too much specification were stil in devedlopment😁')
    if form.validate_on_submit():
            try:
            
                
                api_call=f'https://bible-api.com/{book}%20{chapter}:{verse}'
                params = {
                    'translation': 'kjv'
                }
                headers = {
                    'Authorization': 'Token c0fa75b72d43008250287062a012eea8'
                }
                response = requests.get(api_call, params=params, headers=headers)

                bible=response.json()['text']
                result=f'{book} {chapter}:{verse} says {bible}'
                return render_template('bible.html', result=result, form=form)
            
            except:
                flash('Please you have to be specific😅')
                
    return render_template('bible.html', form=form)

#to do list
@app.route('/todo', methods=['GET', 'POST'])
@login_required
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

@app.route('/todo/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_schedule(id):
    schedule_to_update= ToDO.query.get_or_404(id) 
    form=ToDoList()
    if form.validate_on_submit():
        schedule_to_update.task= form.task.data
        schedule_to_update.date=form.date.data
        db.session.add(schedule_to_update)
        db.session.commit()
        flash('Schedule has been updated')
        return redirect(url_for('schedules'))
    else:
        form.task.data=schedule_to_update.task
        form.date.data=schedule_to_update.date
        return render_template('update_task.html', form=form)


#function for deleting schedules
@app.route('/delete/<int:id>')
def delete(id):
    try:
        task=ToDO.query.get(id)
        db.session.delete(task)
        db.session.commit()
        flash('Task Completed')
        return redirect('/todo')
    except:
        flash('Error deleting task')
        return redirect('/todo')    
     
#function for deleting user           
@app.route('/delete/user/<int:id>')
@login_required
def delete_user(id):
    if current_user.id == id:
        try:
            login=User.query.get(id)
            db.session.delete(login)
            db.session.commit()
            flash('User deleted')
            return redirect(url_for('register'))
        except:
            flash('Error deleting user')
            return redirect(url_for('register'))         


    
#flask stuff
if __name__ =='__main__':
    with app.app_context():
            app.run(debug=True)
    
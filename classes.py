from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Length
class ToDoList(FlaskForm):
    task=StringField('Task', validators=[DataRequired()]) 
    date=StringField('Date to be Completed')
    submit=SubmitField('Submit')

class PasswordForm(FlaskForm):
    password= PasswordField('Password', validators=[DataRequired()])
    submit= SubmitField('Submit')

class RegistrationForm(FlaskForm):
    name= StringField('Full Name', validators=[DataRequired()])
    username=StringField('Username', validators=[DataRequired()])
    password= PasswordField('Password', validators=[DataRequired()])
    password2= PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    key_word= StringField('Enter key word', validators=[DataRequired()])
    submit= SubmitField('Submit')

class UpdateForm(FlaskForm):
    name= StringField('Full Name', validators=[DataRequired()])
    username=StringField('Username', validators=[DataRequired()])
    password_scan= PasswordField('Enter previous password', validators=[DataRequired()])
    password= PasswordField('Enter new password', validators=[DataRequired()])
    password2= PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    key_word= StringField('Enter key word', validators=[DataRequired()])
    submit= SubmitField('Submit')


class LoginForm(FlaskForm):    
    username=StringField('Username', validators=[DataRequired()])
    password= PasswordField('Password', validators=[DataRequired()])
    submit= SubmitField('Submit')
    
class PasswordManager(FlaskForm):  
    password=PasswordField('password', validators=[DataRequired()])
    key_word=PasswordField('Key Word', validators=[DataRequired()])
    submit=SubmitField('Submit')
    
class Enter(FlaskForm):
    site=StringField('Enter what the password is for',validators=[DataRequired()])
    password=PasswordField('Enter password you want to save',validators=[DataRequired()])
    password2=PasswordField('Retype password',validators=[DataRequired(), EqualTo('password')])
    submit= SubmitField('Save')
    
    
class Weather(FlaskForm):
    city=StringField('City', validators=[DataRequired()])
    submit=SubmitField('Search')
    
class Currency(FlaskForm):
    currency1=StringField('Currency 3 code Letter')
    currency2=StringField('Currency 3 code Letter')
    currency3=StringField('Currency 3 code Letter')
    currency4=StringField('Currency 3 code Letter')
    submit=SubmitField('Get')    
    
    
class Bible(FlaskForm):
    book=StringField('Which book of the bible', validators=[DataRequired()])
    chapter=IntegerField('Which chapter of the bible', validators=[DataRequired()])
    verse=IntegerField('Which verse of the bible', validators=[DataRequired()])
    submit=SubmitField('Read')  
    

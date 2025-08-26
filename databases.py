from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_login import UserMixin
from datetime import datetime




app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///task.db'
app.config['SECRET_KEY']="legend"
db=SQLAlchemy(app)







class User(db.Model, UserMixin):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(150), nullable=False)
    username= db.Column(db.String(150), unique=True)    
    password_hash= db.Column(db.String(128))
    key_word=db.Column(db.String(20))
    date=db.Column(db.DateTime, default=datetime.utcnow)

        
class ToDO(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    task=db.Column(db.String(500))
    date=db.Column(db.String(250))
    arrange_by_date= db.Column(db.DateTime, default=datetime.utcnow)
    
class Password(db.Model, UserMixin):
    id= db.Column(db.Integer, primary_key=True)   
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    password= db.Column(db.String(150))
    key_word= db.Column(db.String(20))
    site=db.Column(db.String(120))
    date=db.Column(db.DateTime, default=datetime.utcnow)
    
with app.app_context():
    db.create_all()  
from werkzeug.security import generate_password_hash #generates a unique hashed password to store in the database for security
from flask_sqlalchemy import SQLAlchemy #this is our ORM (Object Relational Mapper)
from flask_login import LoginManager, UserMixin #load user as current_user and class to help us do that
from datetime import datetime #put a timestamp when we create any new object in the database 
import uuid # makes a unique id for our data (primary keys)


# instantiate all of our classes
db = SQLAlchemy() #make our database object
login_manager = LoginManager() #makes login object


# use login_manager object to create our user_loader function
@login_manager.user_loader
def load_user(user_id):
    """
    Given *user_id*, return the associated User object.
    
    :parameter unicode user_id: user_id is user to retrieve
    """
    
    return User.query.get(user_id) # this is probably the most basic query, just grabs the row/object associated with that primary key
                                    # similar to SELECT * FROM user WHERE user_id = user_id


# create our User class/table. Think of these as admin users
class User(db.Model, UserMixin):
    # CREATE TABLE User, house all the columns we create
    user_id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow) # very similar to default CURRENT_DATE in pg 
    
    
    # INSERT INTO, User() Values()
    def __init__(self, username, email, password, first_name="", last_name=""):
        self.user_id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = self.set_password(password)
        
        
    # methods for edditing our attributes
    def set_id(self):
        return str(uuid.uuid4()) #creating random string for our primary key
    
    
    # we need a method to get_id for our user_loader
    def get_id(self):
        return str(self.user_id) #UserMixin grabs user_id to load the current user 
    
    
    def set_password(self, password):
        return generate_password_hash(password) # hashes the password so it is secure
    
    
    def __repr__(self):
        return f"<User: {self.username}>"
    
    
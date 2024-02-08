from werkzeug.security import generate_password_hash #generates a unique hashed password to store in the database for security
from flask_sqlalchemy import SQLAlchemy #this is our ORM (Object Relational Mapper)
from flask_login import LoginManager, UserMixin #load user as current_user and class to help us do that
from datetime import datetime #put a timestamp when we create any new object in the database 
import uuid # makes a unique id for our data (primary keys)
from flask_marshmallow import Marshmallow 


# internal import
from .helpers import get_image 


# instantiate all of our classes
db = SQLAlchemy() #make our database object
login_manager = LoginManager() #makes login object
ma = Marshmallow() # makes marshmallow object


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
    
    
class Product(db.Model):
    # CREATE TABLE
    prod_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String)
    description = db.Column(db.String(200))
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    prodord = db.relationship('ProdOrder', backref = 'product', lazy=True) # establishing relationship between ProdOrder & Product table
    
    # INSERT INTO
    def __init__(self, name, price, quantity, image="", description=""):
        self.prod_id = self.set_id()
        self.name = name
        self.image = self.set_image(image, name)
        self.description = description
        self.price = price
        self.quantity = quantity 
        
    
    def set_id(self):
        return str(uuid.uuid4())
    
    
    def set_image(self, image, name):
        
        if not image: #aka the user did not give us an image
            image = get_image(name) #name is our argument replacing the search parameter in our get_image() function 
            # come back and add the api call 
        
        return image 
    
    # when a customer buys a produce we need to decrement thhe total quantity available 
    def decrement_quantity(self, quantity):
        
        self.quantity -= int(quantity)
        return self.quantity 
    
    
    def increment_quantity(self, quantity):
        
        self.quantity += int(quantity)
        return self.quantity 
    
    
    def __repr__(self):
        return f"<Product: {self.name}>"
        
# only need this for purpose of tracking what customers arae tied to which orders   
class Customer(db.Model):
    # CREATE TABLE
    cust_id = db.Column(db.String, primary_key=True)
    date_created = db.Column(db.DateTime, default = datetime.utcnow())
    prodord = db.relationship('ProdOrder', backref = 'customer', lazy=True)
    
    def __init__(self, cust_id):
        self.cust_id = cust_id # this is coming from the frontend so should be the same
        
    def __repr__(self):
        return f"<Customer: {self.cust_id}>"
    
    
    
class Order(db.Model):
    #CREATE TABLE
    order_id = db.Column(db.String, primary_key=True)
    order_total = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow() )
    prodord = db.relationship('ProdOrder', backref = 'order', lazy=True)
    
    
    def __init__(self):
        self.order_id = self.set_id()
        self.order_total = 0.00 # starting our order off at $0
        
        
    def set_id(self):
        return str(uuid.uuid4())
        
        
    # method to increase our order total
    def increment_ordertotal(self, price):
        
        self.order_total = float(self.order_total)
        self.order_total += float(price)
        
        return self.order_total 
    
    
    # method to decrement the order total for when people update or delete their order 
    def decrement_ordertotal(self, price):
        
        self.order_total = float(self.order_total)
        self.order_total -= float(price)
        
        return self.order_total
    

    def __repr__(self):
        return f"Order: {self.order_id}>"
    
    
    
# example of a join table
# because an Order can have many Products but a Product can be a part of many Orders (many-to-many) relationship
    
    
class ProdOrder(db.Model):
    # CREATE TABLE
    prodorder_id = db.Column(db.String, primary_key=True)
    # first instance of using a foreign key that is a primary key on another table
    prod_id = db.Column(db.String, db.ForeignKey('product.prod_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    order_id = db.Column(db.String, db.ForeignKey('order.order_id'), nullable=False)
    cust_id = db.Column(db.String, db.ForeignKey('customer.cust_id'), nullable=False)
    
    
    # INSERT INTO
    def __init__(self, prod_id, quantity, price, order_id, cust_id):
        self.prodorder_id = self.set_id()
        self.prod_id = prod_id
        self.quantity = quantity # how much quantity of that product the customer is buying
        self.price = self.set_price(quantity, price) # total price of that quantity of product
        self.order_id = order_id
        self.cust_id = cust_id
        
    def set_id(self):
        return str(uuid.uuid4())
    
    
    def set_price(self, quantity, price):
        
        quantity = int(quantity)
        price = float(price)
        
        self.price = quantity * price
        return self.price
    
    
    def update_quantity(self, quantity):
        
        self.quantity = int(quantity)
        return self.quantity
    
    
    
    
    
    


# create our Schema classs (aka what are data will look like when we pass it to the frontend)
# data also cannot be an object but rather a dictionray (json)
    
    
class ProductSchema(ma.Schema):
    
    class Meta:
        fields = ['prod_id', 'name', 'description', 'image', 'price', 'quantity']
        


# instantiate our ProductSchema class so we can use it in our application
product_schema = ProductSchema() # 1 singular product dictionary
products_schema = ProductSchema(many=True) # a list of many product dictionaries 
    
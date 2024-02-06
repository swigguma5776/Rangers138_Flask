from flask import Blueprint, render_template, request, redirect, flash 
from werkzeug.security import check_password_hash 
from flask_login import login_user, logout_user 


# internal imports
from rangers_shop.models import User, db # grabbing our class so we can instantiate User objects
from rangers_shop.forms import RegisterForm, LoginForm 


# instantiate our Blueprint
auth = Blueprint('auth', __name__, template_folder='auth_templates')


# our routes for sign up, sign in, logout
@auth.route('/signup', methods=['GET', 'POST']) #GET request to SEE the form, POST request to POST data to our database 
def signup():
    
    # instantiate our RegisterForm class
    registerform = RegisterForm()
    
    if request.method == 'POST' and registerform.validate_on_submit():
        #grab our data from the submitted form
        first_name = registerform.first_name.data
        last_name = registerform.last_name.data 
        username = registerform.username.data
        email = registerform.email.data
        password = registerform.password.data 
        
        print('Register Form', email, password) # testing that we are getting data from the form
        
        # query into our database to check if the username and/or email already exists 
        
        if User.query.filter(User.username == username).first():
            flash(f"Username {username} already exists. Please Try Again!", category='warning')
            return redirect('/signup')
        if User.query.filter(User.email == email).first():
            flash(f"Email {email} already exists. Please Try Again!", category='warning')
            return redirect('/signup')
        
        # instantiating our user object from User class
        user = User(username, email, password, first_name, last_name)
        
        # we can add this object to our database
        db.session.add(user)
        db.session.commit()
        
        
        flash(f"You have successfully registered user {username}", category='success')
        return redirect('/signin')
    
    return render_template('sign_up.html', form=registerform ) #passing loginform object as form in html 
    
@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    
    # instantiate LoginForm
    loginform = LoginForm()
    
    if request.method == 'POST' and loginform.validate_on_submit():
        email = loginform.email.data
        password = loginform.password.data 
        
        print('Login Form', email, password)
        
        # query to find the user with the same email
        user = User.query.filter(User.email == email).first()  # same as SELECT * FROM user WHERE email = email 
        
        if user and check_password_hash(user.password, password):
            # if this comes back we have validated our user and using UserMixin & load_user() function to load user
            login_user(user) # this makes this user our current_user
            flash(f"Successfully logged in {email}", category='success')
            return redirect('/')
        else:
            flash("Invalid Email and/or Password, Please Try Again!", category='warning')
            return redirect('/signin')
    
    # if its a 'GET' request we need to display this form to the user
    return render_template('sign_in.html', form=loginform ) #passing loginform object as form in html 
    
@auth.route('/logout')
def logout():
    logout_user() #current_user is now None
    return redirect('/')
    
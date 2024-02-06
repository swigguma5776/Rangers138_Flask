from flask import Flask 
from config import Config 
from .blueprints.site.routes import site #importing blueprint object


#instantiate our Flask app
app = Flask(__name__) #is passing in the name of our directory as the name of our app

#going to tell our app what Class to look to for configuration
app.config.from_object(Config)


#creating our first route using the @route decorator
# @app.route("/") #"/" endpoint is standard landing/home page endpoint 
# def hello_world():
#     return "<p>Hello, World!</p>"

app.register_blueprint(site) #pass in site blueprint object to register




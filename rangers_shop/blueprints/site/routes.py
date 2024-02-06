from flask import Blueprint, render_template 


# instantiate our Blueprint class

                                     # location of html files
site = Blueprint('site', __name__, template_folder='site_templates')


# use our site blueprint object to create our routes
@site.route('/')
def shop():
    return render_template('shop.html') # looking inside site_templates folder for a file called shop.html to render




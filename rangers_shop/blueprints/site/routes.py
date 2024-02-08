from flask import Blueprint, flash, redirect, render_template, request 


# internal imports
from rangers_shop.models import Product, Customer, Order, db 
from rangers_shop.forms import ProductForm


# instantiate our Blueprint class

                                     # location of html files
site = Blueprint('site', __name__, template_folder='site_templates')


# use our site blueprint object to create our routes
@site.route('/')
def shop():
    
    # grab all of the products in our database via query
    allprods = Product.query.all() # same as SELECT * FROM products, list of objects from database 
    allcustomers = Customer.query.all()
    allorders = Order.query.all()
    
    shop_stats = {
        'products': len(allprods), # allprods is a list of objects, so counting how many objects
        'customers': len(allcustomers),
        'sales': sum([order.order_total for order in allorders]) #looping through allorders list, order is each object and im grabbing the order_total & summing them all up
    }
    
    
    return render_template('shop.html', shop=allprods, stats=shop_stats) # looking inside site_templates folder for a file called shop.html to render



@site.route('/shop/create', methods=['GET', 'POST'])
def create():
    
    #instantiate our ProductForm class
    
    createform = ProductForm()
    
    if request.method == 'POST' and createform.validate_on_submit():
        #graab our data
        name = createform.name.data
        image = createform.image.data
        description = createform.description.data
        price = createform.price.data 
        quantity = createform.quantity.data 
        
        product = Product(name, price, quantity, image, description) # instantiate our Product object from Product class
        
        
        db.session.add(product)
        db.session.commit()
        
        flash(f"You have successfully created product {name}", category='success')
        return redirect('/')
    
    elif request.method == 'POST':
        flash("We were unable to process your request", category='warning')
        return redirect('/shop/create')
    
    
    return render_template('create.html', form=createform)


@site.route('/shop/update/<id>', methods=['GET', 'POST']) # <parameter> this is how we pass parameters to our routes
def update(id):
    
    # grab our specific product based on the id 
    product = Product.query.get(id) # same as SELECT * FROM product WHERE prod_id = id
    
    # instantiate our form 
    updateform = ProductForm()
    
    if request.method == 'POST' and updateform.validate_on_submit():
        
        product.name = updateform.name.data
        product.image = product.set_image(updateform.image.data, updateform.name.data)
        product.description = updateform.description.data
        product.price = updateform.price.data
        product.quantity = updateform.quantity.data 
        
        # commit our changes
        db.session.commit()
        
        flash(f"You have successfully updated product {product.name}", category='success')
        return redirect('/')
    
    elif request.method == 'POST':
        flash("We were unable to process your request", category='warning')
        return redirect(f'/shop/update/{product.prod_id}')
    
                            #left of = is html, right of = is what its referencing in function
    return render_template('update.html', form=updateform, product=product)
    

@site.route('/shop/delete/<id>')
def delete(id):
    
    # query the databaase to find that product
    product = Product.query.get(id)
    
    db.session.delete(product)
    db.session.commit()
    
    return redirect('/')


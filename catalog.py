from flask import Flask, render_template, url_for, jsonify
from flask import request, flash, redirect, make_response
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, asc
from database_setup import Base, Category, Products, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import urllib

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "The Catalog Application"

# 'check_same_thread': False => avoids SQLAlchemy check same thread requests
# althogh good at security point of view but was annoying while in a
# developent environment, hence turing it off.
engine = create_engine('sqlite:///catalog.db', connect_args={
         'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# =========== OAuth and logged in user Helper Functions ==========


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
                   json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if a user exists, if it doesn't make a new one
    login_session['id'] = getUserID(login_session['email'])
    if login_session['id'] is None:
        login_session['id'] = createUser(login_session)

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<center><img src="'
    output += login_session['picture']
    output += ' " style = "width: 100px; height: 100px;border-radius: 50px;'
    output += 'margin:0px auto"> </center>'
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


#   ===== User Helper Functions ====
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None
#  ===== End of User Helper Functions ====


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    http = httplib2.Http()
    body = {'token': access_token}
    result = http.request(
             "https://accounts.google.com/o/oauth2/revoke",
             method="POST",
             headers={'Content-type': 'application/x-www-form-urlencoded'},
             body=urllib.urlencode(body))[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        flash('You have successfully logged out')
        response = make_response(json.dumps({'status': 'Disconnected'}), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps(result, 400))
        response.headers['Content-Type'] = 'application/json'
        return response
# =========== End of OAuth and logged in user Helper Functions ==========


# =========== Routing Handler Functions ==========
# prevent page caching in browser for all pages
@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0, no-store, must-revalidate'
    # Headers to force browser read only from server even on an event where
    # user press the back and forward buttons.
    return r


# Catches all 404 errors and send user to friendly 404 page.
@app.errorhandler(404)
def not_found(e):
    categories = session.query(Category).all()
    return render_template("404.html", categories=categories,
                           user=login_session)


# routes defalut site root [localhost:5000] to app home [/catalog/]
@app.route('/')
def routeToHome():
    return redirect('/catalog/')
# =========== End of Routing Handler Functions =========


# ================ Application Home Page ===============
@app.route('/catalog/')
def categories():
    # fetches all categroy to use in categrory list menu
    categories = session.query(Category).all()
    # joining using ForeignKey relationship to get parent category
    # reverse ordering by id to get the last 10 product entries
    products = session.query(Products).join(Category).order_by(
            "Products.id desc").limit(10)
    return render_template('home.html', categories=categories,
                           products=products, user=login_session)
# ============== End of Application Home Page ===========


# =============== Category Handler Functions ============

# Retrive all products in a category
@app.route('/catalog/<string:category_name>/<int:category_id>/view/')
def categoryView(category_name, category_id):
    category = session.query(Category).filter_by(id=category_id).first()
    categories = session.query(Category).all()
    products = session.query(Products).filter_by(category_id=category_id).all()
    return render_template('category.html', category=category,
                           products=products, categories=categories,
                           user=login_session)


# Add new categroy
@app.route('/catalog/category/new/', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'POST':  # POST creates the category
        categoryName = request.form.get('txtCategory')
        newCategory = Category(name=categoryName, user_id=login_session['id'])
        session.add(newCategory)
        session.commit()
        flash('Category "'+newCategory.name+'" added to catalog.')
        categories = session.query(Category).all()
        thisCategory = session.query(Category).filter_by(
                  id=newCategory.id).first()
        returnURL = '''/catalog/{0}/{1}/view'''
        return redirect(returnURL.format(thisCategory.name,
                        thisCategory.id))
        # Formats URL and redirects to newly created categroy page
    else:
        # GET displays the UI page to create the categoryEnd of Category
        categories = session.query(Category).all()
        return render_template('_add-category.html', categories=categories)


# Edit category
@app.route('/catalog/<string:category_name>/'
           + '<int:category_id>/edit/', methods=['GET', 'POST'])
def categoryEdit(category_name, category_id):
    if request.method == 'POST':  # POST updates the category
        myCategoryQuery = session.query(Category).filter_by(
                         id=request.form.get('hidCategoryID')).first()
        if myCategoryQuery != []:
            myCategoryQuery.name = request.form.get('txtName')
            session.add(myCategoryQuery)
            session.commit()
            flash('Category updated successfully')
            categories = session.query(Category).all()
            returnURL = '''/catalog/{0}/{1}/edit'''
            return redirect(returnURL.format(myCategoryQuery.name,
                            myCategoryQuery.id))
            # Formats URL and redirects to the updated categroy page
    else:   # GET displays the edit page
        categories = session.query(Category).filter_by(
                     user_id=login_session['id']).all()
        category = session.query(Category).filter_by(id=category_id).first()
        return render_template('edit-category.html', category=category,
                               categories=categories, user=login_session)


# Delete Category
@app.route('/catalog/<string:category_name>/'
           + '<int:category_id>/delete/', methods=['GET', 'POST'])
def categoryDelete(category_name, category_id):
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':  # POST deletes the category
        categoryToDelete = session.query(Category).filter_by(
                          id=request.form.get('hidCategoryID')).first()
        if categoryToDelete != []:
            deletedCategory = categoryToDelete.name
            session.delete(categoryToDelete)

            # delete all products in the category
            productsToDelete = session.query(Products).filter_by(
                 category_id=request.form.get('hidCategoryID')).delete()
            session.commit()
            flash('Category "'+deletedCategory+'" deleted from catalog.')
            categories = session.query(Category).all()
            return render_template('delete-category.html',
                                   category=category_name,
                                   categories=categories, user=login_session)
    else:
        # GET displays the UI page to confirm delete
        categories = session.query(Category).all()
        category = session.query(Category).filter_by(id=category_id).first()
        return render_template('delete-category.html', category=category,
                               categories=categories, user=login_session)

# =============== End of Category Handler Functions =============


# =================== Product Handler Functions =================
# Retrive product details
@app.route('/catalog/<string:category_name>/<string:product_name>/'
           + '<int:product_id>/view/')
def productView(category_name, product_name, product_id):
    categories = session.query(Category).all()
    product = session.query(Products).filter_by(id=product_id).first()
    if product is not None:  # at least one matching product
        return render_template('product.html', category=category_name,
                               product=product, categories=categories,
                               user=login_session)
    else:  # worst case - if no matching product redirect to 404 page
        return redirect('404')


# Add new product
@app.route('/catalog/products/new/', methods=['GET', 'POST'])
def newProduct():
    if request.method == 'POST':  # POST creates a new product
        productName = request.form.get('txtName')
        category = request.form.get('selCategory')
        price = request.form.get('txtPrice')
        description = request.form.get('txtDescription')
        newProduct = Products(name=productName, price=price,
                              description=description, category_id=category,
                              user_id=login_session['id'])
        session.add(newProduct)
        session.commit()
        flash('Product "'+newProduct.name+'" added to catalog.')
        categories = session.query(Category).all()
        product = session.query(Products).filter_by(
                  id=newProduct.id).join(Category).first()
        returnURL = '''/catalog/{0}/{1}/{2}/view'''
        return redirect(returnURL.format(product.category.name,
                        product.name, product.id))
        # Formats URL and redirects to newly created product page
    else:
        # GET displays the UI page to create new product
        categories = session.query(Category).filter_by(
                     user_id=login_session['id']).all()
        return render_template('_add-product.html', categories=categories)


# Edit product
@app.route('/catalog/<string:category_name>/<string:product_name>/'
           + '<int:product_id>/edit/', methods=['GET', 'POST'])
def productEdit(category_name, product_name, product_id):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':  # POST updates the product
        myProductQuery = session.query(Products).filter_by(
                         id=request.form.get('hidProductID')).first()
        if myProductQuery != []:
            myProductQuery.name = request.form.get('txtName')
            myProductQuery.category_id = request.form.get('selCategory')
            myProductQuery.price = request.form.get('txtPrice')
            myProductQuery.description = request.form.get('txtDescription')
            session.add(myProductQuery)
            session.commit()
            flash('Product updated successfully')
            categories = session.query(Category).all()
            product = session.query(Products).filter_by(
                      id=product_id).join(Category).first()
            returnURL = '''/catalog/{0}/{1}/{2}/edit'''
            return redirect(returnURL.format(product.category.name,
                            product.name, product.id))
            # Formats URL and redirects to edit page with changes updated
            # user can continue editing if needed
    else:
        # GET displays the UI page to update the product
        categories = session.query(Category).all()
        product = session.query(Products).filter_by(id=product_id).first()
        return render_template('edit-product.html', category=category_name,
                               product=product, categories=categories,
                               user=login_session)


@app.route('/catalog/<string:category_name>/<string:product_name>/'
           + '<int:product_id>/delete/', methods=['GET', 'POST'])
def productDelete(category_name, product_name, product_id):
    if 'username' not in login_session:
        return redirect('/login')

    if request.method == 'POST':  # POST deletes the category
        myProductQuery = session.query(Products).filter_by(
                         id=request.form.get('hidProductID')).first()
        if myProductQuery != []:
            productToDelete = myProductQuery.name
            session.delete(myProductQuery)
            session.commit()
            flash('Product "'+productToDelete+'" deleted from catalog.')
            categories = session.query(Category).all()
            return render_template('delete-product.html',
                                   category=category_name,
                                   product=request.form.get('txtName'),
                                   categories=categories, user=login_session)
    else:  # GET displays the UI page to confirm delete
        categories = session.query(Category).all()
        product = session.query(Products).filter_by(id=product_id).first()
        return render_template('delete-product.html', category=category_name,
                               product=product, categories=categories,
                               user=login_session)

# =================== End of Product Handler Functions =================


# ==================== JSON EndPoint Handler Functions =================
# JSON endpoint to retrive all categrories
@app.route('/catalog/categories/JSON')
def catgoriesJSON():
    category = session.query(Category).all()
    return jsonify(categories=[i.serialize for i in category])


# JSON endpoint to retrive all products in a category
@app.route('/catalog/category/<int:category_id>/JSON')
def categoryViewEndpoint(category_id):
    category = session.query(Category).filter_by(id=category_id).first()
    products = session.query(Products).filter_by(category_id=category_id).all()
    if category is not None:
        return jsonify(category_products=[i.serialize for i in products])
    else:
        error = {"error": "category not found"}
        return jsonify(error)


# JSON endpoint to retrive product details
@app.route('/catalog/product/<int:product_id>/JSON')
def productViewJSON(product_id):
    categories = session.query(Category).all()
    product = session.query(Products).filter_by(id=product_id).first()
    if product is not None:  # at least one matching product
        return jsonify(product=product.serialize)
    else:
        error = {"error": "no products found"}
        return jsonify(error)

# =================== End of JSON EndPoint Handler Functions =================


if __name__ == '__main__':
    app.secret_key = '\xd3\x97I\rd.`\xee\xfc\xf2\xdf\xf2'
    app.debug = True
    print "Catalog app running at port:5000 Url- http://localhost:5000/catalog"
    app.run(host='0.0.0.0', port=5000)

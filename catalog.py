from flask import Flask, render_template, url_for, jsonify
from flask import request, flash, redirect
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import Base, Category, Products
app = Flask(__name__)
app.secret_key = '\xd3\x97I\rd.`\xee\xfc\xf2\xdf\xf2'

engine = create_engine('sqlite:///catalog.db', connect_args={
         'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# prevent page caching in browser for all pages
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0, no-store, must-revalidate'
    return r


@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
    categories = session.query(Category).all()
    return render_template("404.html", categories=categories)


@app.route('/catalog/')
def categories():
    categories = session.query(Category).all()
    # joining using ForeignKey relationship to get parent category
    # reverse ordering by id to get the last 10 items entries
    products = session.query(Products).join(Category).order_by(
            "Products.id desc").limit(10)
    return render_template('home.html', categories=categories,
                           products=products)


@app.route('/categories/JSON', methods=['GET'])
def catgoriesJSON():
    category = session.query(Category).all()
    return jsonify(categories=[i.serialize for i in category])


@app.route('/catalog/<string:category_name>/<int:category_id>/view/')
def categoryView(category_name, category_id):
    categories = session.query(Category).all()
    products = session.query(Products).filter_by(category_id=category_id).all()
    return render_template('category.html', category=category_name,
                           products=products, categories=categories)


@app.route('/catalog/<string:category_name>/<string:product_name>/'
           + '<int:product_id>/view/')
def productView(category_name, product_name, product_id):
    categories = session.query(Category).all()
    product = session.query(Products).filter_by(id=product_id).first()
    if product is not None:  # at least one matching product
        return render_template('product.html', category=category_name,
                               product=product, categories=categories)
    else:
        return redirect('404')


@app.route('/catalog/<string:category_name>/<string:product_name>/'
           + '<int:product_id>/edit/', methods=['GET', 'POST'])
def productEdit(category_name, product_name, product_id):
    if request.method == 'POST':
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
            # return render_template('edit.html', category=category_name,
            # product=product, categories=categories)
    else:
        categories = session.query(Category).all()
        product = session.query(Products).filter_by(id=product_id).first()
        return render_template('edit.html', category=category_name,
                               product=product, categories=categories)


@app.route('/products/new/', methods=['GET', 'POST'])
def newProduct():
    if request.method == 'POST':
        productName = request.form.get('txtName')
        category = request.form.get('selCategory')
        price = request.form.get('txtPrice')
        description = request.form.get('txtDescription')
        newProduct = Products(name=productName, price=price,
                              description=description, category_id=category)
        session.add(newProduct)
        session.commit()
        return "product added to database"
    else:
        categories = session.query(Category).all()
        return render_template('_add-product.html', categories=categories)


@app.route('/catalog/<string:category_name>/<string:product_name>/'
           + '<int:product_id>/delete/', methods=['GET', 'POST'])
def productDelete(category_name, product_name, product_id):
    if request.method == 'POST':
        myProductQuery = session.query(Products).filter_by(
                         id=request.form.get('hidProductID')).first()
        if myProductQuery != []:
            productToDelete = myProductQuery.name
            session.delete(myProductQuery)
            session.commit()
            flash('Product "'+productToDelete+'" deleted from catalog.')
            categories = session.query(Category).all()
            return render_template('delete.html', category=category_name,
                                   product=request.form.get('txtName'),
                                   categories=categories)
    else:
        categories = session.query(Category).all()
        product = session.query(Products).filter_by(id=product_id).first()
        return render_template('delete.html', category=category_name,
                               product=product, categories=categories)


if __name__ == '__main__':
    app.debug = True
    print "Catalog app running at port:5000 Url- http://localhost:5000/catalog"
    app.run(host='0.0.0.0', port=5000)

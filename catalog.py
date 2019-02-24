from flask import Flask, render_template, url_for, jsonify, request
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import Base, Category, Products
app = Flask(__name__)


engine = create_engine('sqlite:///catalog.db', connect_args={
         'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/catalog/')
def categories():
    categories = session.query(Category).all()
    # joining using ForeignKey relationship to get parent category
    # reverse ordering by id to get the last 10 items entries
    products = session.query(Products).join(Category).order_by(
            "Products.id desc").limit(10)
    return render_template('home.html', categories=categories, products=products)


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
def ProductView(category_name, product_name, product_id):
    categories = session.query(Category).all()
    product = session.query(Products).filter_by(id=product_id).first()
    return render_template('product.html', category=category_name,
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


if __name__ == '__main__':
    app.debug = True
    print "Catalog app running at port:5000 Url- http://localhost:5000/catalog"
    app.run(host='0.0.0.0', port=5000)

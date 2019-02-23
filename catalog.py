from flask import Flask, render_template, url_for, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import Base, Category, Products
app = Flask(__name__)


engine = create_engine('sqlite:///catalog.db', connect_args={
         'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/categories/')
def categories():
    category = session.query(Category).all()
    # joining using ForeignKey relationship to get parent category
    # reverse ordering by id to get the last 10 items entries
    items = session.query(Products).join(Category).order_by(
            "Products.id desc").limit(10)
    return render_template('home.html', category=category, items=items)


@app.route('/categories/JSON')
def catgoriesJSON():
    category = session.query(Category).all()
    items = session.query(Products).order_by("id desc")
    return jsonify(categories=[i.serialize for i in category])


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

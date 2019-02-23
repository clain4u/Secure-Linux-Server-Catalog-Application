from flask import Flask, render_template, url_for
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import Base, Category, Products
app = Flask(__name__)


engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/restaurants/')
def restaurantMenu():
    category = session.query(Category).all()
    items = session.query(Products).limit(2)
    return render_template('home.html', category=category, items=items)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

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


@app.route('/restaurants/')
def catgories():
    category = session.query(Category).all()
    items = session.query(Products).limit(2)
    return render_template('home.html', category=category, items=items)


@app.route('/restaurants/JSON')
def catgoriesJSON():
    category = session.query(Category).all()
    items = session.query(Products).limit(2)
    return jsonify(categories=[i.serialize for i in category])


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

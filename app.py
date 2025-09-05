"""Serves the app on localhost"""
from flask import Flask, render_template, request
import os
from data_models import db, Author, Book

# Init Flask app and connect to database
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
db.init_app(app)


@app.route('/')
def home():
    """Renders the home page"""
    all_books = db.session.query(Book).all()
    return render_template('home.html', books=all_books)


if __name__ == "__main__":
    """
    Resets and create tables
    ‼️To comment after first usage!!
    Then run the Flask app
    """
    #with app.app_context():
    #    db.drop_all()
    #    db.create_all()
    app.run(host="0.0.0.0", port=5005, debug=True)

"""Serves the app on localhost"""
from datetime import datetime
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


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """Form to add a new author to the database"""
    if request.method == 'GET':
        return render_template('add_author.html')

    # POST - Add Author
    name = request.form.get('name')
    birthdate = request.form.get('birthdate')
    death_date = request.form.get('date_of_death')

    # Convert dates to Date objects
    birthdate = datetime.strptime(birthdate, '%Y-%m-%d').date()

    if death_date:
        death_date = datetime.strptime(death_date, '%Y-%m-%d').date()

    new_author = Author(
        name=name,
        birth_date=birthdate,
        date_of_death=death_date if death_date else None
    )
    db.session.add(new_author)
    db.session.commit()

    return render_template('add_author.html', author_name=name)


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """Form to add a new book to the database"""
    all_authors = db.session.query(Author).all()
    if request.method == 'GET':
        return render_template('add_book.html', authors=all_authors)

    # POST - Add Book
    title = request.form.get('title')
    publication_year = int(request.form.get('publication_year')[0:4])
    author_id = request.form.get('author_id')

    # Convert publication_year to int and format YYYY
    new_book = Book(
        title=title,
        publication_year=publication_year,
        author_id=author_id
    )
    db.session.add(new_book)
    db.session.commit()

    return render_template('add_book.html', book_title=title, authors=all_authors)


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

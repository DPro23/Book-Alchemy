"""Serves the app on localhost"""
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
import os
from data_models import db, Author, Book

# Init Flask app and connect to database
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
db.init_app(app)


@app.route('/')
def home():
    """Renders the home page with sorting options"""
    sort = request.args.get('sort')
    search = request.args.get('search')

    # Sorting the results
    if sort:
        sorted_books = []
        if sort == 'author':
            sorted_books = (db.session.query(Book).join(Book.author)
                            .order_by(Author.name.asc()).all())

        elif sort == 'title':
            sorted_books = db.session.query(Book).order_by(
                Book.title.asc()).all()

        elif sort == 'year':
            sorted_books = db.session.query(Book).order_by(
                Book.publication_year.asc()).all()

        return render_template('home.html', books=sorted_books)

    # Sort by keyword
    if search:
        searched_books = db.session.query(Book).filter(Book.title.like('%' + search + '%')).order_by(
            Book.title.asc()).all()

        return render_template('home.html', books=searched_books)

    # Default list
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


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """Delete a book from the database by its id"""
    book = db.session.query(Book).filter_by(id=book_id).first()
    # Book deleted successfully
    if book:
        # msg = f"The Book {book.title} has been deleted successfully."
        db.session.delete(book)
        db.session.commit()
    else:
        # msg = f"The Book with id {book_id} doesn't exist."
        pass

    # Book not found
    return redirect(url_for("home"))


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

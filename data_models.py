""""Define data models"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
    """author model"""
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    birth_date = db.Column(db.Date)
    date_of_death = db.Column(db.Date, nullable=True)



    def __repr__(self):
        return f"Author({self.name}, {self.birth_date}, {self.date_of_death})"


    def __str__(self):
        return f"Author({self.name}, {self.birth_date}, {self.date_of_death})"


class Book(db.Model):
    """book model"""
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.Numeric(precision=13, scale=0), unique=True)
    title = db.Column(db.String)
    publication_year = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey(Author.id))
    author = db.relationship(Author, backref='books', foreign_keys=[author_id])


    def __repr__(self):
        return f"Book({self.isbn}, {self.title}, {self.publication_year})"


    def __str__(self):
        return f"Book({self.isbn}, {self.title}, {self.publication_year})"

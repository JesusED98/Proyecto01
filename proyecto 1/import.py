import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://oxiustss:7_u2OkQ8wyeI2I3q0ziR7nyWfjQJIWlL@balarama.db.elephantsql.com:5432/oxiustss")
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        if(isbn != 'isbn'):
            db.execute("INSERT INTO libros (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",{"isbn": isbn, "title": title, "author": author, "year": year})
    db.commit()
        
if __name__ == "__main__":
    main()
# Import all necessary modules
from flask import Flask, render_template, jsonify, request
import sqlite3

# Create a Flask object
app = Flask(__name__)

# Define the path to the SQLite database
DATABASE = 'Python/Assignment/Flask_Assignment/Intermediate Flask Topics/9.RESTful API using Flask/books.db'

# Set the path to the database in the Flask app configuration
app.config['DATABASE'] = DATABASE


# Ensure that the table 'books' exists in the database
def create_table():
    with app.app_context():
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER NOT NULL
            )
        ''')
        conn.commit()
        conn.close()


# Call the function to create the 'books' table
create_table()


@app.route('/')
def load_page():
    # Render the index.html with the list of books obtained from get_all_books()
    return render_template('index.html', books=get_all_books())


@app.route('/books', methods=['GET'])
def get_all_books():
    # Retrieve all books from the 'books' table in the database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    conn.close()
    # Return the list of books as a JSON response
    return books


@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    # Retrieve a specific book by its ID from the 'books' table
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    book = cursor.fetchone()
    conn.close()
    if book:
        # Return the book details as a JSON response
        return jsonify({'id': book[0], 'title': book[1], 'author': book[2], 'year': book[3]})
    else:
        # Return an error message if the book is not found
        return jsonify({'error': 'Book not found'}), 404
    

@app.route('/books', methods=['POST'])
def add_book():
    # Add a new book to the 'books' table based on the JSON data received
    new_book = request.get_json()
    title = new_book['title']
    author = new_book['author']
    year = new_book['year']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO books (title, author, year) VALUES (?, ?, ?)', (title, author, year))
    conn.commit()
    new_book_id = cursor.lastrowid
    conn.close()

    # Return the details of the newly added book as a JSON response
    return jsonify({'id': new_book_id, 'title': title, 'author': author, 'year': year}), 201


@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    # Update the details of an existing book based on the JSON data received
    updated_book = request.get_json()
    title = updated_book['title']
    author = updated_book['author']
    year = updated_book['year']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('UPDATE books SET title=?, author=?, year=? WHERE id=?', (title, author, year, book_id))
    conn.commit()
    conn.close()

    # Return the updated details of the book as a JSON response
    return jsonify({'id': book_id, 'title': title, 'author': author, 'year': year})


@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    # Delete a book from the 'books' table based on its ID
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM books WHERE id=?', (book_id,))
    conn.commit()
    conn.close()

    # Return a success message as a JSON response
    return jsonify({'message': 'Book deleted successfully'})



if __name__ == '__main__':
    # Run the Flask application
    app.run()
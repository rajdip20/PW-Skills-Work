# Import necessary modules
from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3
import os

# Create a Flask object
app = Flask(__name__)

# Specify the path to the SQLite database file
DATABASE = 'Python/Assignment/Flask_Assignment/Intermediate Flask Topics/7.Perform CRUD Operations/items.db'


# Function to connect to the database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        # Create a new SQLite database connection and set row_factory to retrieve rows as dictionaries
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


# Close the database connection when the request ends
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        # Close the SQLite database connection
        db.close()


# Function to initialize the database with the specified schema
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            # Execute the SQL script to create the database schema
            db.cursor().executescript(f.read())
        db.commit()


# Route to display the list of items
@app.route('/')
def show_items():
    db = get_db()

    # Execute a SQL query to fetch items from the database and order them by ID in descending order
    cursor = db.execute('SELECT id, name FROM items ORDER BY id DESC')

    # Fetch all items from the query result
    items = cursor.fetchall()

    # Render the 'show_items.html' template, passing the items to be displayed
    return render_template('show_items.html', items=items)


# Route to handle adding a new item
@app.route('/add', methods=['POST'])
def add_item():
    db = get_db()
    name = request.form['name']         # Retrieve the name of the new item from the form dat
    db.execute('INSERT INTO items (name) VALUES (?)', (name,))          # Execute a SQL query to insert the new item into the database
    
    db.commit()                             # Commit the changes to the database

    # Redirect to the 'show_items' route to display the updated list of items
    return redirect(url_for('show_items'))


# Route to handle deleting an item
@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    db = get_db()
    # Execute a SQL query to delete the specified item from the database
    db.execute('DELETE FROM items WHERE id = ?', (item_id,))
    
    # Commit the changes to the database
    db.commit()
    # Redirect to the 'show_items' route to display the updated list of items
    return redirect(url_for('show_items'))


# Route to display the form for editing an item
@app.route('/edit/<int:item_id>')
def edit_item(item_id):
    db = get_db()
    # Execute a SQL query to fetch the details of the specified item from the database
    cursor = db.execute('SELECT id, name FROM items WHERE id = ?', (item_id,))
    # Fetch the details of the item from the query result
    item = cursor.fetchone()
    # Render the 'edit_item.html' template, passing the item details to be displayed in the form
    return render_template('edit_item.html', item=item)


# Route to handle updating an item
@app.route('/update/<int:item_id>', methods=['POST'])
def update_item(item_id):
    db = get_db()
    # Retrieve the updated name of the item from the form data
    name = request.form['name']
    # Execute a SQL query to update the name of the specified item in the database
    db.execute('UPDATE items SET name = ? WHERE id = ?', (name, item_id))
    # Commit the changes to the database
    db.commit()
    # Redirect to the 'show_items' route to display the updated list of items
    return redirect(url_for('show_items'))



# Main entry point of the application
if __name__ == '__main__':
    # Configuration settings for the Flask app
    app.config['SECRET_KEY'] = 'secret_key'
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    # Initialize the database if it does not exist
    if not os.path.exists(DATABASE):
        init_db()

    # Run the Flask application
    app.run()
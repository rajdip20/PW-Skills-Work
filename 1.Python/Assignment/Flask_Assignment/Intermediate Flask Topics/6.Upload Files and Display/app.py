# Import necessary modules
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os


# Create a Flask object
app = Flask(__name__)

# Configure folder names and supported file types in the webpage
app.config['UPLOAD_FOLDER'] = 'Python/Assignment/Flask_Assignment/Intermediate Flask Topics/6.Upload Files and Display/uploads'
app.config['FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}


# Verify the allowed files based on file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')         # Define route for the starting page
def load_page():
    files = os.listdir(app.config['UPLOAD_FOLDER'])         # Fetch all existing files in the specified upload folder
    return render_template('index.html', files=files)       # Load the webpage named index.html with the list of files


@app.route('/upload', methods=['POST'])     # Define route for handling file upload
def upload_file():
    # Check if the 'file' key is present in the request
    if 'file' not in request.files:
        return redirect(request.url)

    # Get the file from the request
    file = request.files['file']

    # Check if the filename is empty
    if file.filename == '':
        return redirect(request.url)

    # Check if the file has an allowed extension
    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))         # Save the file to the specified upload folder
         
        # Redirect to the starting page after successful upload
        return redirect(url_for('load_page'))

    return redirect(request.url)        # Redirect to the starting page if the file is not allowed



@app.route('/uploads/<filename>')       # Define route for serving uploaded files
def uploaded_file(filename):
    return send_from_directory(app.config['FOLDER'], filename)


@app.route('/delete/<filename>', methods=['GET', 'POST'])           # Define route for deleting a file
def delete_file(filename):
    
    # Construct the file path based on the upload folder and filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Check if the file exists, and delete it if it does
    if os.path.exists(file_path):
        os.remove(file_path)

    # Redirect to the starting page after deleting the file
    return redirect(url_for('load_page'))


# Main entry point of the application
if __name__ == '__main__':
    # Create the upload folder if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
        
    app.run()           # Run the Flask application
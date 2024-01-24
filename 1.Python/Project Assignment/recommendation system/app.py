# Import necessary modules
from flask import Flask, render_template, request
import requests


# Initializing Flask app
app = Flask(__name__)

# The Movie Database (TMDB) API key and base URL
TMDB_API_KEY = 'YOUR_API_KEY'
TMDB_BASE_URL = 'https://api.themoviedb.org/3'


# Function to get top movies based on genre
def get_top_movies(genre_id, number):
    # Endpoint for discovering movies based on genre
    endpoint = f"{TMDB_BASE_URL}/discover/movie"

    # Parameters for the API request
    params = {
        'api_key': TMDB_API_KEY,
        'with_genres': int(genre_id),
        'sort-by': 'vote_average.desc',     # Sorting by vote average in descending order
        'vote_count.gte': 500               # Considering movies with vote count greater than or equal to 500
    }

    # Making a GET request to TMDB API
    response = requests.get(endpoint, params=params)

    # Checking if the request was successful (status code 200)
    if response.status_code == 200:
        movies = []
        # Extracting movie results from the response from pages 1 to 3
        for page in range(1, 4):
            params['page'] = page       # Add the 'page' parameter to the request

            response = requests.get(endpoint, params=params)

            # Check if the request for the current page was successful
            if response.status_code == 200:
                # Extend the movies list with results from the current page
                movies.extend(response.json().get('results', []))
            else:
                # If the request for the current page was not successful, break the loop
                break

        # Extracting title of top movies according to user input
        top_movies = [movie['title'] for movie in movies[:number]]
        return top_movies
    else:
        # Return an empty list if the request was not successful
        return []


# Route for the home page
@app.route('/')
def load_page():
    return render_template('index.html')


# Route for recommending movies based on selected genre
@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if request.method == 'POST':
        # Getting the selected genre from the form data
        genre = request.form['genre']
        # Splitting the genre into ID and name
        genre_id, genre_name = genre.split(':')

        # Getting the number of top movies from the form data
        number = int(request.form['number'])

        # Calling the function to get top movies based on the selected genre and specified number
        top_movies = get_top_movies(genre_id, number)
        # Rendering the recommendations page with the category (genre), recommended movies the count number
        return render_template('recommendations.html', category=genre_name, recommendations=top_movies, count=number)
    
    else:
        # If the request method is not POST, render the home page
        return render_template('index.html')



# Running the Flask application
if __name__ == '__main__':
    app.run()
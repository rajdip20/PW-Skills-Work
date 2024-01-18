# Import all necessary modules
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests

# Create a Flask object
app = Flask(__name__)


# Function to scrape images from Google Images
def scrape_google(query):
    url = f"https://www.google.com/search?q={query}&sca_esv=596606957&rlz=1C1RXQR_enIN1071IN1072&hl=en&tbm=isch&sxsrf=ACQVn09cyEzEi-mWW1ZpYDfSnw6aQt4NKw:1704735874067&source=lnms&sa=X&ved=2ahUKEwizn9aBrM6DAxWqSGwGHfSEBF0Q_AUoA3oECAEQBQ&cshid=1704736043500682&biw=1536&bih=703&dpr=1.25"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Extract image sources from the 'img' tags in the HTML
    images = [img['src'] for img in soup.find_all('img')][1:]
    return images


# Function to scrape images from wallpapers.com
def scrape_wallpapers(query):
    images = []
    # Loop through multiple pages (1 to 5) on wallpapers.com
    for i in range(1, 6):
        url = f"https://wallpapers.com/search/{query}?p={i}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract image sources from the 'img' tags with class 'promote'
        images.extend([f"https://wallpapers.com{img['data-src']}" for img in soup.find_all('img', 'promote')])
    return images


# Route for the homepage
@app.route('/')
def load_page():
    return render_template('index.html')


# Route for handling search requests
@app.route('/search', methods=['GET', 'POST'])
def search():
    # Get the search query from the form submission
    query = request.form.get('query')
    # Call the scraping functions to get image results
    google_results = scrape_google(query)
    wallpapers_results = scrape_wallpapers(query)
    # Render the result.html template with the query and image results
    return render_template('result.html', query=query, google_results=google_results, wallpapers_results=wallpapers_results)


# Run the Flask app
if __name__ == '__main__':
    app.run()
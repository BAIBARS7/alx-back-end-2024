# reviews/utils.py

import os
import requests
from urllib.parse import quote

def get_movie_details(movie_title):
    """
    Fetch movie details from OMDB API based on the movie title.

    Args:
        movie_title (str): The title of the movie to search for.

    Returns:
        dict or None: A dictionary containing movie details if found, otherwise None.
    """
    api_key = os.getenv('MOVIE_API_KEY')  # Use environment variable for the API key
    if not api_key:
        raise ValueError("API key is missing. Set the MOVIE_API_KEY environment variable.")
    
    # URL encode the movie title to handle spaces and special characters
    encoded_title = quote(movie_title)
    url = f'http://www.omdbapi.com/?t={encoded_title}&apikey={api_key}'  # For OMDB
    # Or for TMDB (uncomment if needed)
    # url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={encoded_title}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        return response.json()  # Movie details as a dictionary
    except requests.exceptions.RequestException as e:
        print(f"Error fetching movie details: {e}")  # Log the error
        return None

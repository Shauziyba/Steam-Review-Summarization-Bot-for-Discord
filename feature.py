import requests
from bs4 import BeautifulSoup

def fetch_game_details(game_id):
    """Fetch game details using the Steam appdetails API."""
    try:
        # Define the Steam API URL using the game_id (Steam App ID)
        url = f"https://store.steampowered.com/api/appdetails?appids={game_id}&l=english"
        
        # Send a GET request to the Steam API
        response = requests.get(url)
        
        # Check if the response status is successful (200 OK)
        if response.status_code != 200:
            print("Error fetching game details")
            return None
        
        # Parse the JSON response from Steam API
        app_details = response.json()
        
        # Check if the response contains valid game details
        if str(game_id) not in app_details or not app_details[str(game_id)]['success']:
            print("Game details not found.")
            return None
        
        # Extract game data from the response
        game_data = app_details[str(game_id)]['data']
        
        # Extract relevant information
        game_title = game_data.get('name', 'Unknown Game')
        game_description = game_data.get('short_description', 'No description available.')
        release_date = game_data.get('release_date', {}).get('date', 'N/A')
        game_price = game_data.get('price_overview', {}).get('final_formatted', 'Free')

        # Extract genres
        genres = [genre['description'] for genre in game_data.get('genres', [])]
        genres_str = ', '.join(genres) if genres else 'No genres available.'

        # Extract categories (e.g., Single Player, Multiplayer, etc.)
        categories = [category['description'] for category in game_data.get('categories', [])]
        categories_str = ', '.join(categories) if categories else 'No categories available.'

        # Extract and clean minimum system requirements (PC)
        pc_requirements = game_data.get('pc_requirements', {}).get('minimum', " ")
        clean_requirements = clean_html(pc_requirements)

        # Extract website URL
        website = game_data.get('website', 'No official website available.')

        # Return the extracted data including categories and cleaned system requirements
        game_details = {
            "Game Title": game_title,
            "Game Description": game_description,
            "Release Date": release_date,
            "Price": game_price,
            "Genres": genres_str,
            "Categories": categories_str,
            "Minimum Requirements": clean_requirements,
            "Website": website,
            "Notes": "The information provided may not be fully up-to-date. For more details, please visit the official Steam store page."
        }
        
        return game_details
    
    except Exception as e:
        print(f"Error fetching game details: {e}")
        return None


def clean_html(html_content):
    """Clean HTML tags and format the minimum requirements."""
    # Use BeautifulSoup to parse and clean the HTML
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Extract the list items, ignoring the tags
    list_items = soup.find_all('li')
    
    # Build a clean formatted list from the extracted list items
    formatted_requirements = []
    for item in list_items:
        text = item.get_text(strip=True)  # Get text and strip surrounding whitespaces
        formatted_requirements.append(text)
    
    # Combine the list items into a clean, human-readable format
    formatted_text = "\n".join(formatted_requirements)
    
    return formatted_text

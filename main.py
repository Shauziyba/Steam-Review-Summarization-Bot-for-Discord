import discord
from discord.ext import commands
import requests
import logging
import random
from steam_review_scraper import search_game_id
from steam_reviews import ReviewLoader
from transformers import PegasusTokenizer, PegasusForConditionalGeneration
from preprocessing import clean_text,correct_grammar
from save_to_excel import save_summary_to_excel
from save_time import measure_execution_time
from feature import fetch_game_details
from evaluating import save_scores_to_excel, evaluate_generated_summary
import nltk
from nltk.tokenize import sent_tokenize
from dotenv import load_dotenv
import os

# Memuat variabel lingkungan dari file .env
load_dotenv()

# Mendapatkan token dari variabel lingkungan
token = os.getenv('DISCORD_TOKEN')

# Define intents
intents = discord.Intents.default()
intents.messages = True  # Enable message-related events
intents.message_content = True  # Enable message content intent

# Set up logging
# logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the Discord bot with the specified intents
bot = commands.Bot(command_prefix='!', intents=intents)

# # Load the Pegasus model and tokenizer
# model_name = "google/pegasus-large"
# tokenizer = PegasusTokenizer.from_pretrained(model_name)
# model = PegasusForConditionalGeneration.from_pretrained(model_name)

# Load the fine-tuned model and tokenizer
model_save_path = "./fine_tuned_pegasus_model_test"
tokenizer = PegasusTokenizer.from_pretrained(model_save_path)
model = PegasusForConditionalGeneration.from_pretrained(model_save_path)

def summarize_reviews(reviews, max_word_count=550):
    reviews_text = "\n".join(reviews)
    words = reviews_text.split()

    # Limit to max_word_count
    if len(words) > max_word_count:
        reviews_text = ' '.join(words[:max_word_count])

    inputs = tokenizer(reviews_text, max_length=1024, return_tensors="pt", truncation=True)

    # Adjust max_length for summary
    summary_ids = model.generate(inputs['input_ids'], max_length=90, num_beams=5, early_stopping=True, length_penalty=2.0)

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    # Further adjust summary for readability (sentence splitting)
    sentences = sent_tokenize(summary)
    
    # Reformat with commas for better flow 
    formatted_summary = ', '.join(sentences[:5])  # Limit to first 5 sentences for conciseness

    return formatted_summary

def fetch_game_title(game_id):
    # Fetch the game details to get the title
    url = f"https://store.steampowered.com/api/appdetails?appids={game_id}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Error fetching game details")
        return None
    
    app_details = response.json()
    
    # Extract the title, check if the response is successful
    if str(game_id) in app_details and app_details[str(game_id)]['success']:
        return app_details[str(game_id)]['data']['name']
    
    print("Game title not found.")
    return "Game Title Placeholder"

def fetch_reviews(game_id, limit):
    reviews = ReviewLoader().set_language('english').load_from_api(game_id, limit)
    reviews_data = reviews.review_dict()  # Should be a list of review dictionaries
    url = f"https://store.steampowered.com/appreviews/{game_id}?language=english&json=1&count={limit}"
    print(url)
    
    # Fetching the reviews
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Error fetching reviews")
        return None
    
    query = response.json()

    # Initialize lists for recommended and not recommended reviews
    recommended_reviews = []
    not_recommended_reviews = []

    # Iterate through the list of review dictionaries
    for review in reviews_data:
        # Check if 'voted_up' is present and is True or False
        if review.get('voted_up') is True:
            recommended_reviews.append(review.get('review'))
        elif review.get('voted_up') is False:
            not_recommended_reviews.append(review.get('review'))

    # Fetch the game title
    game_title = fetch_game_title(game_id)

    # Preprocess the reviews
    recommended_reviews = [clean_text(review) for review in recommended_reviews]
    not_recommended_reviews = [clean_text(review) for review in not_recommended_reviews]

    # Summarize the reviews with a word limit
    positive_summary = summarize_reviews(recommended_reviews, max_word_count=750)
    negative_summary = summarize_reviews(not_recommended_reviews, max_word_count=750)

    # Extract query summary data for percentage calculations
    query_summary = query.get('query_summary', {})
    total_positive = query_summary.get('total_positive', 0)
    total_negative = query_summary.get('total_negative', 0)
    total_reviews = query_summary.get('total_reviews', 0)

    # Calculate percentages based on total counts from query_summary
    recommendation_percentage = (total_positive / total_reviews * 100) if total_reviews else 0
    not_recommended_percentage = (total_negative / total_reviews * 100) if total_reviews else 0
    
    # Formatting the output
    summary = {
        "Game Title": game_title,
        "Positive Reviews": positive_summary if positive_summary else 'No positive reviews found.',
        "Negative Reviews": negative_summary if negative_summary else 'No negative reviews found.',
        "Recommendation Percentage": f"{recommendation_percentage:.0f}%",
        "Not Recommended Percentage": f"{not_recommended_percentage:.0f}%",
        "Notes": [
            "Reviews recommend mostly from players looking for a casual game with a light challenge.",
            "Some criticism focused on the monotony of the game after a long time and the in-app purchase aspect."
        ],
    }
    
    return summary

# Helper functions
def rewrite_summary(summary_text):
    """Format and rewrite summary for natural flow."""
    # Split into sentences for readability
    sentences = sent_tokenize(summary_text)
    formatted_summary = ', '.join(sentences)  # Add commas for flow
    return formatted_summary

def format_summary(summary_text):
    sentences = sent_tokenize(summary_text)
    if len(sentences) > 2:  # If there are multiple sentences
        formatted_summary = '. '.join(sentences[:2]) + '.'  # Summarize the first two sentences for brevity
    else:
        formatted_summary = summary_text
    return formatted_summary

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user.name} (ID: {bot.user.id})')
    print('------')
async def on_command_error(ctx, error):
    logging.error(f"Error occurred in {ctx.command} command: {error}")
    
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Sorry, I don't recognize that command. Please check the command list.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required arguments. Please provide all necessary details.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("One of your arguments is invalid. Please check and try again.")
    else:
        await ctx.send("An unexpected error occurred. Please try again later.")

@bot.command(name='sum')
async def summarize(ctx, *, game_name: str):
    try:
        async def main_process(ctx, game_name):
            await ctx.send("Fetching game review summary, it may take a few minutes...")

            # Debug: Print the game name to check if it's passed correctly
            print(f"Searching for game: {game_name}")

            # Search for game ID based on game name
            game_df = search_game_id(game_name)

            if game_df.empty:
                await ctx.send("Game not found.")
                return

            game_id = game_df.iloc[0]['id']  # Assuming 'id' is the correct column for the game ID
            summary = fetch_reviews(game_id, 500)

            if summary:
                positive_reviews = summary['Positive Reviews']
                negative_reviews = summary['Negative Reviews']

                # Rewrite summaries for better naturalness
                rewritten_positive = format_summary(positive_reviews)
                rewritten_negative = format_summary(negative_reviews)

                # Apply grammar correction
                natural_positive = correct_grammar(rewritten_positive)
                natural_negative = correct_grammar(rewritten_negative)

                # Evaluate the summaries
                eval_positive = evaluate_generated_summary(natural_positive)
                eval_negative = evaluate_generated_summary(natural_negative)

                # Specify the file path to save the scores
                output_excel_path = r'C:\Users\Pegasus\Documents\Pegasus_steam_SUM\Evaluation\rouge_scores.xlsx'
                save_scores_to_excel(eval_positive, output_excel_path)
                save_scores_to_excel(eval_negative, output_excel_path)

                # Save the summary to Excel
                save_summary_to_excel(
                    game_title=summary['Game Title'],
                    positive_review=natural_positive,
                    negative_review=natural_negative,
                    recommended=summary['Recommendation Percentage'],
                    not_recommended=summary['Not Recommended Percentage']
                )

                # Build and send output message
                output_message = (
                    f"**{summary['Game Title']} - Review Summary**\n\n"
                    f"**Positive Reviews:** {natural_positive}.\n\n"
                    f"**Negative Reviews:** {natural_negative}.\n\n"
                    f"**Recommendation Percentage:** {summary['Recommendation Percentage']}\n"
                    f"**Not Recommended Percentage:** {summary['Not Recommended Percentage']}\n\n"
                    f"**Notes:** \n- " + "\n- ".join(summary['Notes']) + "\n"
                )

                # Send the message in chunks if it's too long
                max_length = 2000
                if len(output_message) > max_length:
                    for i in range(0, len(output_message), max_length):
                        await ctx.send(output_message[i:i + max_length])
                else:
                    await ctx.send(output_message)
            else:
                await ctx.send("No reviews found for this game.")
        
        # Measure execution time for the main process
        await measure_execution_time(main_process, ctx, game_name)

    except Exception as e:
        # Catch any other errors (e.g., parsing issues, etc.)
        await ctx.send(f"Oops! I couldn't retrieve the information right now. Please try again later.")
        print(f"Unexpected error: {e}")  # Print the error for debugging
        return

@bot.command(name="info")
async def game_info(ctx, *, game_name: str):
    try:
        # Search for the game ID based on the game name
        game_df = search_game_id(game_name)
        
        if game_df.empty:
            await ctx.send("Game not found. Please check the spelling or try another game.")
            return
        
        game_id = game_df.iloc[0]['id']
        
        # Fetch game details using the game ID
        game_details = fetch_game_details(game_id)
        
        if game_details:
            # Format the game details into a message
            output_message = (
                f"**{game_details['Game Title']} - Game Info**\n\n"
                f"**Description:** {game_details['Game Description']}\n\n"
                f"**Release Date:** {game_details['Release Date']}\n"
                f"**Price:** {game_details['Price']}\n"
                f"**Genres:** {game_details['Genres']}\n\n"
                f"**Categories:** {game_details['Categories']}\n\n"
                f"**Minimum Requirment:** \n{game_details['Minimum Requirements']}\n"
                f"**Website:** {game_details['Website']}\n\n"
                f"**Notes:** {game_details['Notes']}\n"
            )
            await ctx.send(output_message)
        else:
            await ctx.send("Could not retrieve game details.")
    
    except requests.exceptions.RequestException as e:
        # Handle request-related errors (network issues, invalid responses, etc.)
        await ctx.send(f"An error occurred while fetching the game details. Please try again later. ({e})")
        return
    
    except Exception as e:
        # Catch any other errors (e.g., parsing issues, etc.)
        await ctx.send("Oops! I couldn't retrieve the Information right now. Please try again later.")
        print(f"Unexpected error: {e}")
        return

@bot.command(name='topgames')
async def topgames(ctx):
    try:
        # SteamSpy API URL to get the top games
        url = "https://steamspy.com/api.php?request=top100in2weeks"
        response = requests.get(url)
        
        if response.status_code == 200:
            top_games_data = response.json()
            game_names = []
            game_set = set()  # Set to keep track of already seen game names

            # Iterate through the data and extract game names
            for game in top_games_data.values():
                game_name = game['name']
                
                # Check for duplicates using a set
                if game_name not in game_set:
                    game_names.append(f"{len(game_names) + 1}. {game_name}")
                    game_set.add(game_name)

            # Randomly select a number of games between 10 and 15
            number_of_games = random.randint(10, 15)

            # Prepare the output message with a random selection of games
            output_message = "\n".join(game_names[:number_of_games])  # Random games between 10 and 15
            await ctx.send(f"Here are some top games in the Steam app this week:\n\n{output_message}")
        else:
            await ctx.send("Sorry, I couldn't fetch the top games at the moment.")
    except Exception as e:
        await ctx.send("Oops! I couldn't retrieve the top games list right now. Please try again.")
        print(f"Error fetching top games: {e}")

@bot.command(name='commands')
async def help_command(ctx):
    help_message = """
**Steam Review Bot - Help**

Here are the available commands you can use:

1. **!sum <game_name>**  
   Get a summary of the reviews for the specified game on Steam.  
   Example: `!sum Stardew Valley`

2. **!topgames**  
   Get a list of top games from the last 2 weeks.

3. **!gameinfo <game_name>**  
   Get detailed information about a game, such as description, price, release date, etc.

4. **!commands**  
   Display all command list message (you are here!).

---

**Notes:**
- The data is may not always be up-to-date.
- For the most accurate and current game details, check the official Steam store page.

Happy gaming!
"""
    await ctx.send(help_message)

# Run the bot
bot.run(token)



# @bot.command(name='topgame')
# async def topgames(ctx):
#     try:
#         # Steam API URL to get the list of top sellers (based on popularity and sales)
#         url = "https://store.steampowered.com/api/featuredcategories"
#         response = requests.get(url)
        
#         if response.status_code == 200:
#             data = response.json()

#             # Extract the top 10 games (for example, from the "top_sellers" category)
#             top_games = []
#             seen_games = set()  # To track duplicate game names

#             if "top_sellers" in data:
#                 top_sellers = data["top_sellers"]["items"][:10]  # Take top 10 games
#                 for game in top_sellers:
#                     game_name = game['name']
#                     if game_name not in seen_games:  # Check if the game name is already in the list
#                         top_games.append(f"{len(top_games) + 1}. {game_name}")
#                         seen_games.add(game_name)  # Add the game to the set to track it

#                 # Send the list of top games in a message
#                 if top_games:
#                     output_message = "\n".join(top_games)
#                     await ctx.send(f"Here are the top games currently:\n\n{output_message}")
#                 else:
#                     await ctx.send("Couldn't find any unique games in the top sellers.")
#             else:
#                 await ctx.send("Couldn't find the top sellers in the data.")
#         else:
#             await ctx.send("Sorry, I couldn't fetch the top games at the moment.")
#     except Exception as e:
#         await ctx.send("An error occurred while fetching the top games.")
#         print(f"Error fetching top games: {e}")


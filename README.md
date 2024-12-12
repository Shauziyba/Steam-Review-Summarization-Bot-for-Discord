# Steam-Review-Summarization-Bot-for-Discord

This project is a Discord bot designed to summarize user reviews from Steam games using an advanced text summarization model (PEGASUS). It processes both positive and negative reviews, providing insights on the sentiment and overall feedback of the games.

## Steam Review Bot

This project is a Discord bot that fetches and summarizes Steam game reviews. It provides functionalities like reviewing Steam games, displaying game information, and listing top games.

## Source Code

You can find the source code for this project in the following files:

- `main.py`: The main bot script with commands.

## Installation Instructions

Follow these steps to set up the project locally:

1. **Clone the repository** to your local machine:

   ```bash
   git clone https://github.com/yourusername/steam-review-bot.git
   ```

2. **Navigate to the project directory**:

   ```bash
   cd steam-review-bot
   ```

3. **Install the required Python libraries**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** in the project directory with your bot token and any necessary API keys:

   ```bash
   DISCORD_TOKEN=your_discord_bot_token
   ```

5. **Run the bot**:
   ```bash
   python main.py
   ```

## Usage / Program Manual

Once the bot is up and running, you can interact with it using the following commands:

1. **!sum `<game_name>`** - Get a summary of the reviews for a specified game on Steam.
   - Example: `!sum Stardew Valley`
2. **!topgames** - Get a list of the top 10 most popular games in the last 2 weeks.

3. **!gameinfo `<game_name>`** - Get detailed information about a game (e.g., description, release date, price, etc.).

4. **!commands** - Show the list of all available commands.

### Sample Data (Optional)

If needed, you can include sample data for testing the bot. Download sample Steam data from [Steam API Sample Data](link_to_data).

## Additional Resources / Dependencies

- **Discord API**: The bot requires the Discord API to send and receive messages. Make sure to add your bot token.
- **Steam API**: The bot interacts with the Steam API for fetching game details and reviews.

## Troubleshooting

If you encounter any issues, check the following:

- Make sure all required environment variables (e.g., bot token, API keys) are set.
- Ensure that your Discord bot has the necessary permissions on the server.

## Questions?

If you have any questions or need assistance, feel free to open an issue or contact me directly.

---

## FAQs

- **How do I set up the bot?**
  Follow the installation instructions provided above.

- **What APIs does the bot use?**
  The bot fetches data from the Steam API and Discord API.

- **Can I add the bot to my own server?**
  Yes, you can add the bot to any Discord server you have administrative access to. Follow the invitation link for your bot and grant the necessary permissions.

- **How can I contribute to this project?**
  Feel free to fork the repository, create a branch, and submit pull requests. Contributions are always welcome!

---

## Notes

- The bot fetches data from Steam's official API, and some information might not be up-to-date.
- For more detailed game info, visit the Steam store page.

---

## Contact and Support

If you have any further questions or run into issues, please feel free to open an issue on GitHub or reach out directly via email.

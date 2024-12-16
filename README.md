# Steam-Review-Summarization-Bot-for-Discord

This project is a Discord bot designed to summarize user reviews from Steam games using an advanced text summarization model (PEGASUS). It processes both positive and negative reviews, providing insights on the sentiment and overall feedback of the games.

## Steam Review Bot

This project is a Discord bot that fetches and summarizes Steam game reviews. It provides functionalities like reviewing Steam games, displaying game information, and listing top games.

## Features

- Fetch and summarize Steam game reviews.
- Display game information like description, release date, and price.
- Provide a list of the top trending Steam games.

---

## Source Code

You can find the source code for this project in the following files:

- `main.py`: The main bot script with commands.

---

## Installation Instructions

### Step 1: Set Up Discord and a Server

1. **Download Discord**  
   If you don’t already have Discord installed, download it from [Discord's official website](https://discord.com/).

2. **Create a Discord Server**
   - Open Discord and log in to your account.
   - Click the **+** button on the left-hand side of the Discord app to create a new server.
   - Follow the on-screen prompts to name and configure your server.

---

### Step 2: Set Up the Discord Developer Portal

1. **Visit the Discord Developer Portal**  
   Go to [Discord Developer Portal](https://discord.com/developers/applications) and log in using your Discord account.

2. **Create a New Application**

   - Click the **New Application** button.
   - Give your application a name (e.g., "Steam Review Bot") and click **Create**.

3. **Generate a Bot Token**

   - In your application settings, go to the **Bot** section on the left-hand menu.
   - Click **Add Bot** and confirm.
   - Copy the **token** provided. This token is needed to authenticate your bot. **Keep it secret!**

4. **Invite the Bot to Your Server**
   - In the Developer Portal, go to the **OAuth2** section and select **URL Generator**.
   - Under **Scopes**, select **bot**.
   - Under **Bot Permissions**, select the permissions your bot requires (e.g., "Send Messages," "Read Message History," etc.).
   - Copy the generated URL, paste it into your browser, and select your server to invite the bot.

---

### Step 3: Installation Instructions

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

## Additional Resources / Dependencies

- **Discord API**: The bot requires the Discord API to send and receive messages. Make sure to add your bot token.
- **Steam API**: The bot interacts with the Steam API for fetching game details and reviews.

## Troubleshooting

If you encounter any issues, check the following:

- Make sure all required environment variables (e.g., bot token, API keys) are set.
- Ensure that your Discord bot has the necessary permissions on the server.

---

## Notes

- The bot fetches data from Steam's official API, and some information might not be up-to-date.
- For more detailed game info, visit the Steam store page.

---

## Contact and Support

If you have any further questions or run into issues, please feel free to open an issue on GitHub or reach out directly via email.

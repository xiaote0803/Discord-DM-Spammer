# Discord Bot Spammer

A Python tool to spam Discord users with multiple bots concurrently

## Support

Join our Discord server for support and updates: [Discord Link](https://discord.gg/R7ybdvBSuM)

## Features

- Concurrent multi-bot messaging
- Configurable message content and count
- Unlimited bot support
- Rate-limit bypass with multiple bots
- Dynamic DM channel creation
- Slash commands and text commands

## Installation

```bash
pip install discord.py python-dotenv
```

## Usage

```bash
python bot.py
```

## Configuration

### .env file

```
MAIN_TOKEN=your_main_bot_token
BOT_1_TOKEN=your_bot_1_token
BOT_2_TOKEN=your_bot_2_token
# Add more BOT_x_TOKEN as needed
GUILD_ID=your_guild_id
```

### config.json

```json
{
  "message_count": 5,
  "message_content": "Message"
}
```

## Bot Setup

1. Create multiple Discord bots on the [Discord Developer Portal](https://discord.com/developers/applications)
2. Copy each bot's token to the `.env` file
3. Configure message settings in `config.json`
4. Run the bot

## Commands

- `/send @user` - Send configured message to user via all other bots

## Disclaimer

This project is for educational purposes only. Use at your own risk. Users are responsible for complying with Discord's Terms of Service and all applicable laws. Spamming may result in account bans or other penalties.

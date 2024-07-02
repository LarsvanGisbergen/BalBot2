# Game Tracker & Betting Discord Bot

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Discord](https://img.shields.io/badge/Discord-Py-blue.svg)

## Overview

Welcome to the Game Tracker & Betting Discord Bot project! This bot allows users to track live games, place bets, and manage scores directly through Discord. When a player is in a new live game, the bot notifies the channel and users can bet on the game outcome using reactions.

## Features

- **Live Game Tracking:** Monitor active games of specified players.
- **Betting System:** Users can place bets on game outcomes through Discord reactions.
- **Score Management:** Automatically updates player scores based on game results.
- **Discord Notifications:** Sends messages to a Discord channel about game statuses and results.

## Prerequisites

- Python 3.8+
- Discord account and a server where you have permission to add bots.

## Player Information

Update `players.json` with player details:
```json
{
    "players": [
        {"name": "Player1", "tag": "Tag1"},
        {"name": "Player2", "tag": "Tag2"},
        {"name": "Player3", "tag": "Tag3"}
    ]
}
``` 

## Main Components

### Main Script (`main.py`)
Handles the core logic for tracking games and communicating with the Discord bot.

### Discord Bot (`bot.py`)
Manages Discord interactions, sending messages, and handling user reactions.

## Interacting with the Bot

1. **Starting the Bot:** Ensure you have set up your environment variables correctly and run `main.py`. The bot will start and connect to your Discord server.
2. **Placing Bets:** When a player starts a new game, the bot sends a message to the specified channel. Users can place bets by reacting to the message.
3. **Game Outcome:** Once the game ends, the bot updates the scores and sends a summary message with the results, listing the winners and losers with their respective scores.

Enjoy tracking and betting on your favorite games with this Discord bot!

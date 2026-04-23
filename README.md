# Daily Weather Report Telegram Bot

A Python automation bot that fetches daily weather reports and sends them to a Telegram chat. Designed for easy deployment on Replit.

## Features

- Fetches weather data from OpenWeatherMap API
- Sends formatted weather reports to Telegram
- Configurable location and units
- Error handling and logging
- Health check endpoint for Replit
- Ready for daily scheduling via Replit cron jobs

## Setup Instructions

### 1. Prerequisites

- A Replit account (free tier works)
- OpenWeatherMap API key (free at https://openweathermap.org/api)
- Telegram Bot Token (create via @BotFather on Telegram)
- Telegram Chat ID (use @userinfobot to get your chat ID)

### 2. Deploy on Replit

1. Create a new Python Repl
2. Copy the files from this project:
   - `main.py`
   - `requirements.txt`
   - `.env.example` (rename to `.env`)
3. Install dependencies automatically or run `pip install -r requirements.txt`

### 3. Configure Environment Variables

In Replit, go to the **Secrets** tab (lock icon) and add:

```
WEATHER_API_KEY = "your_openweathermap_api_key"
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"
TELEGRAM_CHAT_ID = "your_telegram_chat_id"
CITY = "Delhi"  # Optional, defaults to Delhi
COUNTRY_CODE = "IN"  # Optional, defaults to India
UNITS = "metric"  # Optional, defaults to metric (Celsius)
```

### 4. Run the Bot

Click the **Run** button. The bot will:
1. Send an initial weather report
2. Start a health check server on port 8000
3. Be ready for scheduled runs

### 5. Schedule Daily Reports

To run the bot daily on Replit:

**Option A: Using Replit Cron (Recommended)**
1. Create a `.replit` file with:
   ```
   run = "python main.py"
   ```
2. In Replit, use the **Tools** → **Cron Jobs** feature to schedule daily execution

**Option B: Manual Scheduling**
Uncomment the while loop in `main.py` to run every 24 hours continuously.

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `WEATHER_API_KEY` | OpenWeatherMap API key | Yes | - |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot token from @BotFather | Yes | - |
| `TELEGRAM_CHAT_ID` | Telegram chat ID to send messages to | Yes | - |
| `CITY` | City name for weather | No | Delhi |
| `COUNTRY_CODE` | Country code (ISO 3166) | No | IN |
| `UNITS` | Temperature units (metric/imperial) | No | metric |

## Project Structure

- `main.py` - Main bot logic with weather fetching and Telegram integration
- `requirements.txt` - Python dependencies
- `.env.example` - Template for environment variables

## How It Works

1. The bot fetches current weather data from OpenWeatherMap API
2. Formats the data into a readable message with emojis
3. Sends the message to the configured Telegram chat using Markdown
4. Includes error handling for API failures and network issues
5. Provides a health endpoint for Replit monitoring

## Customization

- Change the city/country by updating `CITY` and `COUNTRY_CODE` env vars
- Modify `format_weather_message()` in `main.py` to change the message format
- Adjust units (Celsius/Fahrenheit) with the `UNITS` env var

## Troubleshooting

- **No messages received**: Check Telegram bot token and chat ID
- **Weather data missing**: Verify OpenWeatherMap API key and city name
- **Bot not running**: Check Replit logs for error messages
- **Port issues**: Ensure port 8000 is available or change `PORT` env var

## License

MIT License - Free to use and modify.

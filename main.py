import os
import requests
import logging
from datetime import datetime
from telegram import Bot
from telegram.error import TelegramError
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WeatherBot:
    """
    A bot that fetches weather data and sends it to Telegram.
    """
    
    def __init__(self):
        """Initialize the bot with environment variables."""
        self.weather_api_key = os.getenv('WEATHER_API_KEY')
        self.telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.city = os.getenv('CITY', 'Delhi')  # Default to Delhi if not set
        self.country_code = os.getenv('COUNTRY_CODE', 'IN')  # Default to India
        self.units = os.getenv('UNITS', 'metric')  # metric for Celsius
        
        if not all([self.weather_api_key, self.telegram_bot_token, self.telegram_chat_id]):
            raise ValueError("Missing required environment variables. Check WEATHER_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID.")
        
        self.weather_url = f"http://api.openweathermap.org/data/2.5/weather"
        self.bot = Bot(token=self.telegram_bot_token)
    
    def get_weather_data(self):
        """
        Fetch weather data from OpenWeatherMap API.
        Returns a dictionary with weather info or None on error.
        """
        params = {
            'q': f'{self.city},{self.country_code}',
            'appid': self.weather_api_key,
            'units': self.units
        }
        try:
            response = requests.get(self.weather_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('cod') != 200:
                logger.error(f"Weather API error: {data.get('message', 'Unknown error')}")
                return None
            
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch weather data: {e}")
            return None
        except ValueError as e:
            logger.error(f"Invalid JSON response: {e}")
            return None
    
    def format_weather_message(self, weather_data):
        """
        Format weather data into a readable message for Telegram.
        """
        if not weather_data:
            return "Unable to fetch weather data at the moment."
        
        city = weather_data.get('name', 'Unknown')
        country = weather_data.get('sys', {}).get('country', '')
        temp = weather_data.get('main', {}).get('temp', 'N/A')
        feels_like = weather_data.get('main', {}).get('feels_like', 'N/A')
        humidity = weather_data.get('main', {}).get('humidity', 'N/A')
        description = weather_data.get('weather', [{}])[0].get('description', 'N/A')
        wind_speed = weather_data.get('wind', {}).get('speed', 'N/A')
        
        # Get current date and time
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        
        message = (
            f"🌤️ *Daily Weather Report* 🌤️\n"
            f"📅 Date: {date_str}\n"
            f"⏰ Time: {time_str}\n"
            f"📍 Location: {city}, {country}\n\n"
            f"🌡️ Temperature: {temp}°C\n"
            f"🤔 Feels Like: {feels_like}°C\n"
            f"💧 Humidity: {humidity}%\n"
            f"🌬️ Wind Speed: {wind_speed} m/s\n"
            f"☁️ Conditions: {description.capitalize()}\n\n"
            f"_Data provided by OpenWeatherMap_"
        )
        return message
    
    def send_telegram_message(self, message):
        """
        Send a message to the configured Telegram chat.
        """
        try:
            self.bot.send_message(chat_id=self.telegram_chat_id, text=message, parse_mode='Markdown')
            logger.info("Weather report sent successfully to Telegram.")
            return True
        except TelegramError as e:
            logger.error(f"Failed to send Telegram message: {e}")
            return False
    
    def run_daily_report(self):
        """
        Main function to fetch weather and send to Telegram.
        """
        logger.info("Starting daily weather report...")
        weather_data = self.get_weather_data()
        message = self.format_weather_message(weather_data)
        success = self.send_telegram_message(message)
        
        if success:
            logger.info("Daily weather report completed successfully.")
        else:
            logger.error("Failed to complete daily weather report.")
        
        return success

class HealthCheckHandler(BaseHTTPRequestHandler):
    """Simple HTTP handler for health checks on Replit."""
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Weather Bot is running')
    
    def log_message(self, format, *args):
        # Suppress default log messages
        pass

def start_health_server():
    """Start a simple HTTP server for health checks on Replit."""
    port = int(os.getenv('PORT', 8000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    logger.info(f"Health check server started on port {port}")
    server.serve_forever()

def main():
    """Main entry point for the weather bot."""
    try:
        # Initialize the bot
        weather_bot = WeatherBot()
        
        # Run the daily report immediately on start
        logger.info("Running initial weather report...")
        weather_bot.run_daily_report()
        
        # For daily automation on Replit, you can:
        # 1. Use Replit's cron job feature (set in .replit file)
        # 2. Use a while loop with sleep for 24 hours
        # 3. Use threading to run the bot periodically
        
        # Example: Run every 24 hours (86400 seconds)
        # Uncomment below for continuous running on Replit
        # while True:
        #     time.sleep(86400)
        #     weather_bot.run_daily_report()
        
        # For now, just run once and keep health server alive
        logger.info("Initial report sent. Bot is ready for scheduled runs via Replit cron.")
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        logger.info("Please set the required environment variables in Replit Secrets.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    # Start health check server in a separate thread for Replit
    health_thread = threading.Thread(target=start_health_server, daemon=True)
    health_thread.start()
    
    # Run main bot logic
    main()
    
    # Keep the main thread alive for health server
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")

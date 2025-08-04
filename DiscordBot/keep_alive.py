"""
Keep Alive Web Server for Discord Bot
Provides a simple web endpoint to keep the bot running on hosting platforms
"""

from flask import Flask
from threading import Thread
import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    """Health check endpoint"""
    return {
        "status": "alive",
        "message": "Free Fire Discord Bot is running",
        "bot": "nezuko-chan#3779"
    }

@app.route('/health')
def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "Free Fire Discord Bot",
        "endpoints": ["/", "/health"]
    }

def run():
    """Run the Flask app"""
    app.run(host='0.0.0.0', port=5000, debug=False)

def keep_alive():
    """Start the web server in a separate thread"""
    logger.info("Starting keep-alive web server on port 5000")
    t = Thread(target=run, daemon=True)
    t.start()
    logger.info("Keep-alive web server started")
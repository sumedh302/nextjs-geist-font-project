"""
Configuration management for Free Fire Discord Bot
"""

import json
import os
from typing import Dict, List, Optional

class BotConfig:
    """Bot configuration manager"""
    
    # Bot settings
    PREFIX = "!"
    DEFAULT_DAILY_LIMIT = 5
    
    # API settings
    API_BASE_URL = "https://likexthug.vercel.app/like"
    API_KEY = "GREAT"
    
    # Region mappings
    REGION_MAP = {
        "ind": "ind",
        "india": "ind",
        "br": "nx",
        "brazil": "nx",
        "us": "nx",
        "usa": "nx",
        "sac": "nx",
        "na": "nx",
        "nx": "nx",
        "me": "ag",
        "middle_east": "ag",
        "ag": "ag"
    }
    
    # Error messages
    MESSAGES = {
        "daily_limit": "❌ **Daily Limit Reached**\nYou've reached your daily limit of **{limit}** requests. Try again tomorrow!",
        "invalid_channel": "❌ This command can only be used in designated channels. Please use one of the allowed channels.",
        "invalid_uid": "❌ **Invalid UID**\nPlease provide a valid UID (numbers only, minimum 6 characters).",
        "invalid_region": "❌ **Invalid Region**\nSupported regions: `IND`, `BR`, `US`, `ME`, `SAC`, `NA`",
        "api_error": "❌ **API Error**\nFailed to connect to Free Fire services. Please try again later.",
        "max_likes": "❌ **Maximum Likes Reached**\nThis UID has already received the maximum likes today.",
        "missing_params": "❌ **Missing Parameters**\nUsage: `/like <uid> <region>` or `!like <uid> <region>`\n\nExample: `/like 123456789 IND`"
    }
    
    def __init__(self):
        """Initialize configuration"""
        self.config_file = "data/config.json"
        self.config_data = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
        
        # Return default config
        return {
            "allowed_channels": [],
            "admin_users": [],
            "unlimited_users": [],
            "daily_limits": {}
        }
    
    def save_config(self):
        """Save configuration to file"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(self.config_data, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get_allowed_channels(self) -> List[int]:
        """Get list of allowed channel IDs"""
        return self.config_data.get("allowed_channels", [])
    
    def is_channel_allowed(self, channel_id: int) -> bool:
        """Check if channel is allowed for commands"""
        allowed_channels = self.get_allowed_channels()
        return len(allowed_channels) == 0 or channel_id in allowed_channels
    
    def get_admin_users(self) -> List[int]:
        """Get list of admin user IDs"""
        return self.config_data.get("admin_users", [])
    
    def is_admin_user(self, user_id: int) -> bool:
        """Check if user is an admin"""
        return user_id in self.get_admin_users()
    
    def get_unlimited_users(self) -> List[int]:
        """Get list of unlimited user IDs"""
        return self.config_data.get("unlimited_users", [])
    
    def is_unlimited_user(self, user_id: int) -> bool:
        """Check if user has unlimited usage"""
        return user_id in self.get_unlimited_users()
    
    def get_user_daily_limit(self, user_id: int) -> int:
        """Get daily limit for specific user"""
        user_limits = self.config_data.get("daily_limits", {})
        return user_limits.get(str(user_id), self.DEFAULT_DAILY_LIMIT)
    
    def set_user_daily_limit(self, user_id: int, limit: int):
        """Set daily limit for specific user"""
        if "daily_limits" not in self.config_data:
            self.config_data["daily_limits"] = {}
        
        self.config_data["daily_limits"][str(user_id)] = limit
        self.save_config()
    
    def add_allowed_channel(self, channel_id: int):
        """Add channel to allowed list"""
        if "allowed_channels" not in self.config_data:
            self.config_data["allowed_channels"] = []
        
        if channel_id not in self.config_data["allowed_channels"]:
            self.config_data["allowed_channels"].append(channel_id)
            self.save_config()
    
    def remove_allowed_channel(self, channel_id: int):
        """Remove channel from allowed list"""
        allowed_channels = self.config_data.get("allowed_channels", [])
        if channel_id in allowed_channels:
            allowed_channels.remove(channel_id)
            self.save_config()

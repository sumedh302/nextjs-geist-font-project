"""
User database management for Free Fire Discord Bot
Handles user daily limits and usage tracking
"""

import json
import os
from datetime import datetime, date
from typing import Dict, Optional

class UserDatabase:
    """User data management system"""
    
    def __init__(self):
        """Initialize user database"""
        self.db_file = "data/users.json"
        self.users_data = self._load_database()
    
    def _load_database(self) -> Dict:
        """Load user database from file"""
        try:
            if os.path.exists(self.db_file):
                with open(self.db_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading user database: {e}")
        
        return {}
    
    def _save_database(self):
        """Save user database to file"""
        try:
            os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
            with open(self.db_file, 'w') as f:
                json.dump(self.users_data, f, indent=2)
        except Exception as e:
            print(f"Error saving user database: {e}")
    
    def get_user_data(self, user_id: int) -> Dict:
        """Get user data or create new entry"""
        user_id_str = str(user_id)
        today = str(date.today())
        
        if user_id_str not in self.users_data:
            self.users_data[user_id_str] = {
                "daily_usage": {
                    "date": today,
                    "count": 0
                },
                "total_usage": 0,
                "first_used": today,
                "last_used": today
            }
            self._save_database()
        
        return self.users_data[user_id_str]
    
    def get_user_daily_usage(self, user_id: int) -> Dict:
        """Get user's daily usage data"""
        user_data = self.get_user_data(user_id)
        daily_usage = user_data.get("daily_usage", {})
        
        today = str(date.today())
        
        # Reset daily usage if it's a new day
        if daily_usage.get("date") != today:
            daily_usage = {
                "date": today,
                "count": 0
            }
            user_data["daily_usage"] = daily_usage
            self._save_database()
        
        return daily_usage
    
    def increment_user_usage(self, user_id: int):
        """Increment user's daily and total usage"""
        user_data = self.get_user_data(user_id)
        daily_usage = self.get_user_daily_usage(user_id)
        
        # Increment counters
        daily_usage["count"] += 1
        user_data["total_usage"] = user_data.get("total_usage", 0) + 1
        user_data["last_used"] = str(date.today())
        
        self._save_database()
    
    def check_user_daily_limit(self, user_id: int, limit: int) -> bool:
        """Check if user has exceeded daily limit"""
        daily_usage = self.get_user_daily_usage(user_id)
        return daily_usage.get("count", 0) < limit
    
    def get_user_remaining_requests(self, user_id: int, limit: int) -> int:
        """Get remaining requests for user"""
        daily_usage = self.get_user_daily_usage(user_id)
        used = daily_usage.get("count", 0)
        return max(0, limit - used)
    
    def reset_user_daily_usage(self, user_id: int):
        """Reset user's daily usage (admin function)"""
        user_data = self.get_user_data(user_id)
        today = str(date.today())
        
        user_data["daily_usage"] = {
            "date": today,
            "count": 0
        }
        self._save_database()
    
    def get_user_stats(self, user_id: int) -> Dict:
        """Get comprehensive user statistics"""
        user_data = self.get_user_data(user_id)
        daily_usage = self.get_user_daily_usage(user_id)
        
        return {
            "daily_used": daily_usage.get("count", 0),
            "total_used": user_data.get("total_usage", 0),
            "first_used": user_data.get("first_used"),
            "last_used": user_data.get("last_used"),
            "current_date": daily_usage.get("date")
        }
    
    def get_all_users_stats(self) -> Dict:
        """Get statistics for all users"""
        stats = {
            "total_users": len(self.users_data),
            "active_today": 0,
            "total_requests": 0
        }
        
        today = str(date.today())
        
        for user_data in self.users_data.values():
            stats["total_requests"] += user_data.get("total_usage", 0)
            
            daily_usage = user_data.get("daily_usage", {})
            if daily_usage.get("date") == today and daily_usage.get("count", 0) > 0:
                stats["active_today"] += 1
        
        return stats

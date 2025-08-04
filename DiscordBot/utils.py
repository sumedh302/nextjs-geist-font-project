"""
Utility functions for Free Fire Discord Bot
"""

import re
import discord
from typing import Optional, Tuple

class BotUtils:
    """Utility functions for the bot"""
    
    @staticmethod
    def validate_uid(uid: str) -> bool:
        """Validate Free Fire UID format"""
        if not uid:
            return False
        
        # Remove any non-digit characters
        clean_uid = re.sub(r'\D', '', uid)
        
        # Check if it's all digits and at least 6 characters
        return len(clean_uid) >= 6 and clean_uid.isdigit()
    
    @staticmethod
    def clean_uid(uid: str) -> str:
        """Clean and format UID"""
        return re.sub(r'\D', '', uid)
    
    @staticmethod
    def validate_region(region: str) -> bool:
        """Validate region code"""
        if not region:
            return False
        
        valid_regions = [
            'ind', 'india', 'br', 'brazil', 'us', 'usa', 
            'sac', 'na', 'nx', 'me', 'middle_east', 'ag'
        ]
        
        return region.lower() in valid_regions
    
    @staticmethod
    def normalize_region(region: str) -> str:
        """Normalize region name for display"""
        region_display = {
            'ind': 'INDIA',
            'india': 'INDIA',
            'br': 'BRAZIL',
            'brazil': 'BRAZIL',
            'us': 'USA',
            'usa': 'USA',
            'sac': 'SAC',
            'na': 'NORTH AMERICA',
            'nx': 'NORTH AMERICA',
            'me': 'MIDDLE EAST',
            'middle_east': 'MIDDLE EAST',
            'ag': 'MIDDLE EAST'
        }
        
        return region_display.get(region.lower(), region.upper())
    
    @staticmethod
    def create_error_embed(title: str, description: str, color: int = 0xE74C3C) -> discord.Embed:
        """Create standardized error embed"""
        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
            timestamp=discord.utils.utcnow()
        )
        return embed
    
    @staticmethod
    def create_success_embed(title: str, description: str, color: int = 0x2ECC71) -> discord.Embed:
        """Create standardized success embed"""
        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
            timestamp=discord.utils.utcnow()
        )
        return embed
    
    @staticmethod
    def format_like_response(player_data: dict, likes_data: dict, limit_info: str) -> str:
        """Format the like response text"""
        return (
            f"```\n"
            f"┌  ACCOUNT\n"
            f"├─ NICKNAME: {player_data.get('nickname', 'Unknown')}\n"
            f"├─ UID: {player_data.get('uid', 'Unknown')}\n"
            f"├─ REGION: {player_data.get('region', 'Unknown')}\n"
            f"└─ RESULT:\n"
            f"    ├─ ADDED: +{likes_data.get('added_by_api', 0)}\n"
            f"    ├─ BEFORE: {likes_data.get('before', 'N/A')}\n"
            f"    └─ AFTER: {likes_data.get('after', 'N/A')}\n"
            f"┌  DAILY LIMIT\n"
            f"└─ {limit_info}\n"
            f"```"
        )
    
    @staticmethod
    def parse_command_args(ctx, region: Optional[str] = None, uid: Optional[str] = None) -> Tuple[Optional[str], Optional[str]]:
        """Parse and swap command arguments if needed"""
        # Handle case where UID is passed as region parameter
        if uid is None and region and region.isdigit():
            uid, region = region, None
        
        return region, uid
    
    @staticmethod
    def is_slash_command(ctx) -> bool:
        """Check if command was invoked as slash command"""
        return hasattr(ctx, "interaction") and ctx.interaction is not None
    
    @staticmethod
    def get_supported_regions() -> str:
        """Get formatted string of supported regions"""
        return "`IND`, `BR`, `US`, `ME`, `SAC`, `NA`"

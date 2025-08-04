# Free Fire Discord Bot

## Overview

A Discord bot that integrates with Free Fire game services to send likes to players. The bot provides a daily limit system for user requests, supports multiple regions, and includes administrative controls for channel restrictions and user permissions. Users can send likes to Free Fire players by providing a UID and region through Discord commands.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Bot Framework
- **Discord.py**: Uses the discord.py library with command extensions for both slash commands and traditional prefix commands
- **Hybrid Commands**: Supports both slash commands (`/like`) and prefix commands (`!like`) for user flexibility
- **Intents Configuration**: Enables message content, guild, and member intents for full functionality

### Command System
- **Cog-based Architecture**: Commands are organized in separate cogs (FreeFireCog) for modularity
- **Input Validation**: Validates UIDs (minimum 6 digits) and regions before processing
- **Error Handling**: Comprehensive error messages for invalid inputs, API failures, and permission issues

### Data Storage
- **File-based Database**: Uses JSON files for persistent storage without external database dependencies
- **User Tracking**: Stores daily usage counts, total usage, and user join dates
- **Configuration Management**: Separate config file for bot settings, channel permissions, and user limits

### Rate Limiting System
- **Daily Limits**: Configurable per-user daily request limits with reset at midnight
- **Unlimited Users**: Special permission system for bypassing daily limits
- **Admin Controls**: Administrative users can modify limits and permissions

### External API Integration
- **Free Fire API**: Integrates with likexthug.vercel.app API for sending likes
- **Region Mapping**: Maps user-friendly region names to API endpoints (IND→ind, BR/US→nx, ME→ag)
- **Async HTTP**: Uses aiohttp for non-blocking API requests with proper session management

### Permission System
- **Channel Restrictions**: Configurable allowed channels for command usage
- **User Roles**: Three user types - regular users, unlimited users, and admin users
- **Validation Layers**: Multiple validation checks for UIDs, regions, limits, and permissions

### Logging and Monitoring
- **Comprehensive Logging**: File and console logging for debugging and monitoring
- **Error Tracking**: Detailed error logging for API failures and system issues
- **Usage Analytics**: Tracks user activity and command usage patterns

## External Dependencies

### Discord Integration
- **discord.py**: Core Discord bot framework
- **Discord API**: Real-time messaging and command handling

### Free Fire Services
- **Like API**: External API at likexthug.vercel.app for sending game likes
- **Region Endpoints**: Multiple regional servers (ind, nx, ag) for global support

### HTTP Client
- **aiohttp**: Asynchronous HTTP client for API requests
- **Session Management**: Persistent HTTP sessions for efficient API communication

### File System
- **JSON Storage**: Local file-based storage for user data and configuration
- **Log Files**: File-based logging system for error tracking and debugging

### Environment Variables
- **DISCORD_BOT_TOKEN**: Discord bot authentication token from environment
# 🛡️ Webixly Security Bot --- Usage Guide

## 📋 Overview

**Webixly Security Bot** is an advanced Discord security bot that
automatically detects and bans users who spam, mention too many members,
or send messages in restricted channels.\
It also logs every moderation action in a specified modlog channel.

------------------------------------------------------------------------

## ⚙️ Setup Instructions

### 1. Create a `.env` file

Inside the same folder as your bot script, create a `.env` file with the
following content:

``` env
DISCORD_TOKEN=YOUR_BOT_TOKEN_HERE
MODLOG_CHANNEL_ID=YOUR_MODLOG_CHANNEL_ID
```

-   **DISCORD_TOKEN** → Your Discord bot token (from [Discord Developer
    Portal](https://discord.com/developers/applications))\
-   **MODLOG_CHANNEL_ID** → The ID of the channel where moderation logs
    will be sent

------------------------------------------------------------------------

### 2. Install Dependencies

Run this command in your terminal:

``` bash
pip install discord.py python-dotenv
```

------------------------------------------------------------------------

### 3. Run the Bot

Start the bot using:

``` bash
python bot.py
```

You should see something like:

    ✅ Logged in as Webixly Security Bot (ID: 123456789012345678)

------------------------------------------------------------------------

## ⚡ Commands

  -------------------------------------------------------------------------------
  Command                     Description                Permission
  --------------------------- -------------------------- ------------------------
  `!ping`                     Checks if the bot is       Everyone
                              online                     

  `!setrestricted #channel`   Sets a restricted channel  Admin only
                              where sending messages     
                              will trigger an **instant  
                              ban**                      
  -------------------------------------------------------------------------------

------------------------------------------------------------------------

## 🚫 Restricted Channel Behavior

Once you set a restricted channel using `!setrestricted #channel`: - The
bot will **pin a warning message** automatically. - Anyone (not in
whitelist) who sends a message in that channel will: 1. Have their
message deleted\
2. Be **automatically banned** 3. Have their recent messages (last 5
minutes) deleted

------------------------------------------------------------------------

## 🔄 Auto-Spam Detection

The bot automatically detects and bans users who: - Send too many
messages too fast\
- Send duplicate messages repeatedly\
- Mention too many users at once

Default thresholds (editable in `config.json`):

``` json
{
  "msg_threshold": 5,
  "time_window": 7,
  "duplicate_threshold": 4,
  "mention_threshold": 5,
  "delete_history_minutes": 5
}
```

------------------------------------------------------------------------

## 📁 Files

  -----------------------------------------------------------------------
  File                       Purpose
  -------------------------- --------------------------------------------
  `bot.py`                   Main bot script

  `.env`                     Environment variables

  `config.json`              Stores settings (restricted channel, spam
                             config, whitelist)
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 🧩 Example Usage

``` bash
!setrestricted #security-zone
```

➡️ Anyone sending a message in `#security-zone` will be instantly
banned.\
All actions are logged in the modlog channel.

------------------------------------------------------------------------

## 🪪 Credits

Developed by **Pablo --- Webixly Security**\
Secure, Smart, and Automatic Discord Protection.

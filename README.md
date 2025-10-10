```
█░█ ▀█▀ █▀▀ █▄▄ █ █▄░█
▀▄▀ ░█░ ██▄ █▄█ █ █░▀█
```

# Webixly Security Bot

**⚡ Discord Auto-Defense System — Hacker Style Edition**

[![repo](https://img.icons8.com/ios-filled/20/FFFFFF/github.png)](https://github.com/yourusername/yourrepo) [![python](https://img.icons8.com/ios-filled/20/FFFFFF/python.png)](https://www.python.org/) [![discord](https://img.icons8.com/ios-filled/20/FFFFFF/discord-logo.png)](https://discord.com/developers) [![license](https://img.icons8.com/ios-filled/20/FFFFFF/certificate.png)](./LICENSE)

```
██╗    ██╗███████╗██████╗ ██╗██╗  ██╗██╗  ██╗██╗  ██╗
██║    ██║██╔════╝██╔══██╗██║╚██╗██╔╝██║ ██╔╝╚██╗██╔╝
██║ █╗ ██║█████╗  ██████╔╝██║ ╚███╔╝ █████╔╝  ╚███╔╝ 
██║███╗██║██╔══╝  ██╔══██╗██║ ██╔██╗ ██╔═██╗  ██╔██╗ 
╚███╔███╔╝███████╗██║  ██║██║██╔╝ ██╗██║  ██╗██╔╝ ██╗
 ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
```

## 📋 Overview

**Webixly Security Bot** is a powerful Discord security system that blocks spam, mass mentions, message floods, and unauthorized activity automatically. Every action is logged in the modlog channel.

## ⚙️ Requirements

* Python 3.8+
* Libraries:

  * `discord.py`
  * `python-dotenv`

## 🚀 Installation & Run

1. Clone the repo:

```bash
git clone https://github.com/webixly/webixly-security-bot.git
cd webixly-security-bot
```

2. (Optional) Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\\Scripts\\activate   # Windows
```

3. Install dependencies:

```bash
pip install discord.py python-dotenv
```

4. Create a `.env` file:

```env
DISCORD_TOKEN=YOUR_BOT_TOKEN_HERE
RESTRICTED_CHANNEL_ID=1234567899999999999
MODLOG_CHANNEL_ID=1234567899999999999
GUILD_ID=123456789012345678
```

5. Run the bot:

```bash
python discordBot.py
```

Expected output:

```
✅ Logged in as Webixly Security Bot (ID: 123456789012345678)
```

## 🛠️ Features

* Automatic spam detection & banning
* Restricted channels with instant ban
* Duplicate/rapid message defense
* Mass mention detection
* Message history wipe on ban
* Full moderation logs

## ⚡ Commands

### ✅ 1. `!ping`

Check if the bot is online.

```
!ping
```

Response:

```
🏓 Pong! Bot is online and secured.
```

### ✅ 2. `!setrestricted` *(Admin Only)*

Set a protected channel where any message sent triggers an instant ban.

```
!setrestricted #channel
```

Or:

```
!setrestricted channel_name
```

What happens:

* Saves channel as restricted
* Pins automatic warning
* Any user message triggers:

  1. Message deletion
  2. Cleanup of history
  3. Instant ban
  4. Log entry

## 🚫 Restricted Channel Behavior

When you set a channel as restricted:

* A pinned warning is created
* Any message sent triggers:

  1. Message deletion
  2. Instant ban
  3. Removal of last 5 minutes of messages
  4. Log in modlog channel

## 🔄 Anti-Spam Config (`config.json`)

```json
{
  "msg_threshold": 5,
  "time_window": 7,
  "duplicate_threshold": 4,
  "mention_threshold": 5,
  "delete_history_minutes": 5
}
```

## 📂 File Structure

* `bot.py` — main script
* `.env` — environment variables
* `config.json` — settings

## 🧪 Example

```bash
!setrestricted #security-zone
```

Anyone typing there gets banned instantly + logs recorded.

## 🤝 Contributing

Feel free to open Issues or PRs. Follow existing code style and include clear descriptions.

## 🪪 License

MIT License — use freely with credit.

## 🔥 Credits

Developed by **Pablo — Webixly Security**
Secure • Smart • Automatic

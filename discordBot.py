import discord
from discord.ext import commands
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from collections import deque, defaultdict
import json
import asyncio

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
MODLOG_CHANNEL_ID = int(os.getenv("MODLOG_CHANNEL_ID", "0"))
CONFIG_FILE = "config.json"

DEFAULT_SPAM_CONFIG = {
    "msg_threshold": 5,
    "time_window": 7,
    "duplicate_threshold": 4,
    "mention_threshold": 5,
    "delete_history_minutes": 5
}

user_msg_history = defaultdict(lambda: deque())

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                pass
    cfg = {
        "restricted_channel_id": None,
        "whitelist": [],
        "spam_config": DEFAULT_SPAM_CONFIG
    }
    save_config(cfg)
    return cfg

def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)

cfg = load_config()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)


async def send_modlog(event_type: str, user: discord.User, reason: str, channel: discord.TextChannel = None, deleted_count: int = 0):
    if MODLOG_CHANNEL_ID == 0:
        return

    modlog_channel = bot.get_channel(MODLOG_CHANNEL_ID)
    if not modlog_channel:
        print("⚠️ Modlog channel not found.")
        return

    color_map = {
        "Restricted": discord.Color.red(),
        "Spam": discord.Color.orange(),
        "Mentions": discord.Color.purple(),
        "Other": discord.Color.blurple()
    }
    color = color_map.get(event_type, discord.Color.dark_red())

    embed = discord.Embed(
        title=f"🚨 {event_type} Auto-Action",
        color=color,
        timestamp=datetime.utcnow()
    )
    embed.set_author(name=f"{user} ({user.id})", icon_url=user.display_avatar.url if user.display_avatar else None)
    embed.add_field(name="🕵️ Reason", value=reason, inline=False)

    if channel:
        embed.add_field(name="💬 Channel", value=f"{channel.mention} (`{channel.id}`)", inline=True)

    if deleted_count:
        embed.add_field(name="🗑️ Deleted Messages", value=str(deleted_count), inline=True)

    embed.set_footer(text="Anti-Spam Security System • Webixly Security", icon_url="https://cdn-icons-png.flaticon.com/512/681/681392.png")

    try:
        await modlog_channel.send(embed=embed)
    except Exception as e:
        print(f"[❌ MODLOG ERROR] {e}")


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

    restricted_id = cfg.get("restricted_channel_id")
    if restricted_id:
        channel = bot.get_channel(restricted_id)
        if channel:
            async for m in channel.history(limit=30):
                if m.pin and m.author == bot.user:
                    try:
                        await m.unpin()
                    except:
                        pass

            embed = discord.Embed(
                title="🚫 Restricted Channel Warning",
                description="**⚠️ Do NOT send any messages in this channel.**\n"
                            "Anyone who sends a message here will be **automatically banned** "
                            "and their recent messages will be deleted.",
                color=discord.Color.red()
            )
            embed.set_footer(text="Anti-Spam Security System • Webixly Security")
            embed.timestamp = datetime.utcnow()
            try:
                msg = await channel.send(embed=embed)
                await msg.pin()
                print(f"⚠️ Warning pinned in #{channel.name}")
            except Exception as e:
                print("Could not pin warning:", e)


def check_spam_trigger(user_id: int, now_ts: float, content: str, spam_cfg):
    dq = user_msg_history[user_id]
    while dq and (now_ts - dq[0][0]) > spam_cfg["time_window"]:
        dq.popleft()

    if len(dq) >= spam_cfg["msg_threshold"]:
        return ("rate", f"{len(dq)} messages in {spam_cfg['time_window']}s")

    if spam_cfg["duplicate_threshold"] > 1:
        same = sum(1 for ts, msg in dq if msg == content)
        if same >= spam_cfg["duplicate_threshold"]:
            return ("duplicate", f"{same} identical messages")

    return None


async def bulk_delete_user_recent_messages(guild: discord.Guild, user: discord.User, minutes: int):
    cutoff = datetime.utcnow() - timedelta(minutes=minutes)
    deleted = 0
    for channel in guild.text_channels:
        perms = channel.permissions_for(guild.me)
        if not (perms.read_message_history and perms.manage_messages and perms.view_channel):
            continue
        try:
            async for m in channel.history(after=cutoff, limit=500):
                if m.author.id == user.id:
                    try:
                        await m.delete()
                        deleted += 1
                        await asyncio.sleep(0.02)
                    except:
                        pass
        except Exception:
            pass
    return deleted


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    user_id = message.author.id
    now = datetime.utcnow()
    now_ts = now.timestamp()
    spam_cfg = cfg.get("spam_config", DEFAULT_SPAM_CONFIG)

    restricted_id = cfg.get("restricted_channel_id")
    if restricted_id and message.channel.id == restricted_id:
        if message.content.startswith("!") or user_id in cfg.get("whitelist", []):
            await bot.process_commands(message)
            return

        try:
            await message.delete()
        except:
            pass

        deleted_count = await bulk_delete_user_recent_messages(message.guild, message.author, spam_cfg.get("delete_history_minutes", 5))

        try:
            await message.guild.ban(message.author, reason="Sent message in restricted channel")
            await send_modlog("Restricted", message.author, "Sent message in restricted channel", message.channel, deleted_count)
        except Exception as e:
            print("Ban failed:", e)
            await send_modlog("Other", message.author, f"❌ Failed to ban: {e}")
        return

    if user_id in cfg.get("whitelist", []):
        await bot.process_commands(message)
        return

    mention_count = len(message.mentions) if hasattr(message, "mentions") else 0
    if mention_count >= spam_cfg.get("mention_threshold", 9999):
        try:
            await message.delete()
        except:
            pass
        deleted_count = await bulk_delete_user_recent_messages(message.guild, message.author, spam_cfg.get("delete_history_minutes", 5))
        try:
            await message.guild.ban(message.author, reason="Mass mentions / spam")
            await send_modlog("Mentions", message.author, f"Mass mentions: {mention_count}", message.channel, deleted_count)
        except Exception as e:
            print("Ban failed:", e)
            await send_modlog("Other", message.author, f"❌ Failed to ban: {e}")
        return

    dq = user_msg_history[user_id]
    dq.append((now_ts, message.content))

    trigger = check_spam_trigger(user_id, now_ts, message.content, spam_cfg)
    if trigger:
        ttype, tinfo = trigger
        try:
            await message.delete()
            deleted_count = await bulk_delete_user_recent_messages(message.guild, message.author, spam_cfg.get("delete_history_minutes", 5))
            await message.guild.ban(message.author, reason=f"AutoSpam trigger: {ttype} ({tinfo})")
            await send_modlog("Spam", message.author, f"Spam trigger: {ttype} ({tinfo})", message.channel, deleted_count)
        except Exception as e:
            print("Auto-ban failed:", e)
            await send_modlog("Other", message.author, f"❌ Failed to auto-ban: {e}")
        user_msg_history.pop(user_id, None)
        return

    if len(dq) > 200:
        while len(dq) > 200:
            dq.popleft()

    await bot.process_commands(message)


@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("🏓 Pong! Bot is online and secured.")


@bot.command(name="setrestricted")
@commands.has_permissions(administrator=True)
async def setrestricted(ctx, *, channel_input: str):
    channel = None
    if ctx.message.channel_mentions:
        channel = ctx.message.channel_mentions[0]
    else:
        name = channel_input.replace("#", "").strip()
        channel = discord.utils.get(ctx.guild.text_channels, name=name)
    if not channel:
        await ctx.send(f"❌ Channel not found: `{channel_input}`")
        return

    cfg["restricted_channel_id"] = channel.id
    save_config(cfg)

    embed = discord.Embed(title="✅ Restricted Channel Set",
                          description=f"Messages sent in {channel.mention} will now trigger an **instant ban**.",
                          color=discord.Color.green())
    await ctx.send(embed=embed)

    warn_embed = discord.Embed(
        title="🚫 Restricted Channel Warning",
        description="**⚠️ Do NOT send any messages here.**\n"
                    "Violating this rule will result in an **automatic ban**.",
        color=discord.Color.red()
    )
    warn_embed.set_footer(text="Anti-Spam Security System • Webixly Security")
    warn_embed.timestamp = datetime.utcnow()
    try:
        wmsg = await channel.send(embed=warn_embed)
        await wmsg.pin()
    except Exception as e:
        print("Pin failed:", e)


if __name__ == "__main__":
    if TOKEN is None:
        print("❌ Error: DISCORD_TOKEN not set in .env")
    else:
        bot.run(TOKEN)

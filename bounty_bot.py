# git add .
# git commit -m "Your commit message here"
# git push origin main


import discord
from discord.ext import commands
from datetime import datetime
from flask import Flask
import os

# Initialize Flask app for HTTP server
app = Flask(__name__)

# Intents for accessing message content and member information
intents = discord.Intents.default()
intents.message_content = True

# Bot setup
bot = commands.Bot(command_prefix="!", intents=intents)

# Create bounty embed with customizable color and uptime field
def create_bounty_embed(title, link, reason, reward, description, poster, uptime, color=discord.Color(0x4f0707)):
    timestamp = int(datetime.utcnow().timestamp())
    uptime_timestamp = timestamp - (uptime * 86400)

    embed = discord.Embed(
        title=title,
        color=color
    )
    embed.add_field(name="Profile Link", value=f"{link}", inline=False)
    embed.add_field(name="Reason", value=f"{reason}", inline=False)
    embed.add_field(name="Reward", value=f"{reward}", inline=False)
    embed.add_field(name="Description", value=f"{description}", inline=False)
    embed.add_field(name="Uptime", value=f"<t:{uptime_timestamp}:R>", inline=False)
    embed.set_footer(text=f"Posted By: {poster}")

    return embed

# Command to post bounty
@bot.command(name="post_bounty")
async def post_bounty(ctx, channel_id: int, title: str, link: str, reason: str, reward: str, description: str, role_id: int, uptime: int):
    if uptime < 14 or uptime > 50:
        await ctx.send("Invalid uptime. Please specify an uptime between 14 and 50 days.")
        return

    channel = bot.get_channel(channel_id)
    if not channel:
        await ctx.send("Invalid channel ID. Please ensure the bot can access the channel.")
        return

    role = discord.utils.get(ctx.guild.roles, id=role_id)
    if not role:
        await ctx.send("Role not found. Please ensure the role ID is correct.")
        return

    role_mention = f"<@&{role_id}>"

    embed = create_bounty_embed(title, link, reason, reward, description, ctx.author.name, uptime)

    await channel.send(f"{role_mention} Bounty posted by {ctx.author.mention}:")
    await channel.send(embed=embed)
    await ctx.send(f"Bounty posted successfully in <#{channel_id}>.")

# Bot event to signal readiness
@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")

# Vercel HTTP route to keep the bot alive
@app.route("/")
def home():
    return "Bot is online!"

# Run the bot
@app.before_first_request
def before_first_request():
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

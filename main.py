import discord
from discord import app_commands
from discord.ext import commands
import os

client = commands.Bot(command_prefix = "!", intents = discord.Intents.all())

cogs = ["cogs.trading"]

@client.event
async def on_ready():
    for cog in cogs:
        await client.load_extension(cog)
    
    print("Bot is ready")
    
    
@client.command()
@commands.is_owner()
async def sync(ctx):
    
    print("Attempting to sync commands...")
    await ctx.send("Attempting to sync commands...")

    try:
        synced = await client.tree.sync()
        await ctx.send(f"Synced {len(synced)} commands.")
    
    except Exception as e:
        await ctx.send(f"Failed to sync commands: {e}")
        print(f"Error syncing commands: {e}")

@client.command()
async def get_server_icon(ctx):
    if ctx.guild:
        icon_url = ctx.guild.icon.url if ctx.guild.icon else "No icon"
        await ctx.send(f"Server Icon URL: {icon_url}")
    else:
        await ctx.send("This command can only be used in a server.")
        


client.run(os.getenv("DISCORD_TOKEN"))
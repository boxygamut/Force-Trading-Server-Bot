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
async def sync(ctx):
    
    try:
        synced = await client.tree.sync()
        await ctx.send(f"Synced {len(synced)} commands.")
    
    except Exception as e:
        await ctx.send(f"Failed to sync commands: {e}")
        print(f"Error syncing commands: {e}")
        
        


client.run(os.getenv("DISCORD_TOKEN"))
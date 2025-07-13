import discord
from discord import app_commands
from discord.ext import commands
import json
import random
from typing import List
from datetime import datetime
import pytz



class Vouch(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.vouch_log_channel = self.client.get_channel(1393229968175140965)

    async def generate_vouch_id(self) -> str:
        
        return str(random.randint(100000, 999999))

    @app_commands.command(name="vouch", description="Vouch for a user")
    async def vouch(self, interaction: discord.Interaction, user: discord.Member, comment: str):
        vouch_id = await self.generate_vouch_id()

        vouch_data = {
            "user_id": str(user.id),
            "comment": comment,
            "vouch_id": vouch_id,
            "vouched_by": str(interaction.user.id),
            "vouched_by_name": interaction.user.name,
            "timestamp": int(datetime.now(pytz.utc).timestamp())
        }

        with open("data/vouches.json", "r") as f:
            vouches = json.load(f)

        if str(user.id) not in vouches["vouches"]:
            vouches["vouches"][str(user.id)] = {}

        vouches["vouches"][str(user.id)][vouch_id] = vouch_data
        
        vouches["vouch_ids"].append(vouch_id)

        with open("data/vouches.json", "w") as f:
            json.dump(vouches, f, indent=4)

        await interaction.response.send_message(f"Vouched for {user.mention}: `{comment}`", ephemeral = True)

        embed = discord.Embed(title="New Vouch", description=f"{interaction.user.mention} vouched for {user.mention} with comment:\n\n`{comment}`", color=0x5ae880)
        embed.set_footer(text = f"Vouch ID: {vouch_id}")

        await self.vouch_log_channel.send(embed=embed)
        
        
    @app_commands.command(name="view_vouches", description="View vouches for a user")
    async def view_vouches(self, interaction: discord.Interaction, user: discord.Member):
        with open("data/vouches.json", "r") as f:
            vouches = json.load(f)

        user_vouches = []
        
        if str(user.id) not in vouches["vouches"]:
            await interaction.response.send_message(f"{user.mention} has no vouches.", ephemeral=True)
            return
        
        for vouch_id, vouch in vouches["vouches"][str(user.id)].items():
            user_vouches.append(vouch)
            
        if len(user_vouches) == 0: # Too bloated? Integrate with first check eventually
            await interaction.response.send_message(f"{user.mention} has no vouches.", ephemeral=True)
            return
        
        vouch_count = len(user_vouches)
        user_vouches = reversed(user_vouches[-5:])
        
        embed_text = "```ansi\n"
        embed_text += f"\u001b[37mStatistics:\n"
        embed_text += f"\u001b[1;32mTotal Vouch Count\u001b[37m: {vouch_count}\n"
        embed_text += f"\u001b[37m▬▬▬▬▬▬▬▬\n"
        
        for vouch in user_vouches:
            embed_text += f"\u001b[0;33m[#{vouch['vouch_id']}] \u001b[37mVouch by {vouch['vouched_by_name']}\u001b[0m\n"
            embed_text += f"\u001b[2;34mUser\u001b[37m: {user.name}\n"
            embed_text += f"\u001b[2;34mComment\u001b[37m: {vouch['comment']}\n"
            embed_text += f"\u001b[37m▬▬▬▬▬▬▬▬\n"
            
        embed_text = embed_text[:-14] + "```"

        embed = discord.Embed(title=f"Most Recent Vouches for {user.name}", description = embed_text, color=0x5ae880)
        # embed.set_footer(text = f"Vouches are displayed most recent at the top")

        await interaction.response.send_message(embed = embed, ephemeral = False)
        
        
        
async def setup(client: commands.Bot):
    await client.add_cog(Vouch(client))
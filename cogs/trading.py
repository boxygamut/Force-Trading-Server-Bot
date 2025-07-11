import discord
from discord import app_commands
from discord.ext import commands
import json
from cogs.constant import constants
import random
from typing import List


class Trading(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        
        
    async def generate_listing_id(self, existing_ids: list):
        unique_id: bool = False
        random_id: int
        
        while not unique_id:
            random_id = random.randint(1000000, 9999999)
            if random_id not in existing_ids:
                unique_id = True
                
        return random_id
    
    async def listings_autocomplete(self, interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        with open("data/listings.json", "r") as f:
            listings = json.load(f)
        
        choices = []
        
        user_id_str = str(interaction.user.id)
        
        if user_id_str not in listings["listings"].keys():
            listings["listings"][user_id_str] = {"listings": {}}

        for listing_id in listings["listings"][user_id_str]["listings"].keys():
                choices.append(listing_id)
                
        return [
            app_commands.Choice(name=choice, value=choice)
            for choice in choices if current.lower() in choice.lower()
        ][:25]

    @app_commands.command(name = "create_listing", description = "Create a new trade listing")
    @app_commands.choices(listing_item = constants["item_choices"])
    @app_commands.choices(wanted_item = constants["item_choices"])
    async def create_listing(self, interaction: discord.Interaction, listing_item: app_commands.Choice[str], listing_quantity: int, wanted_item: app_commands.Choice[str], wanted_quantity: int = 1):

        with open("data/listings.json", "r") as f:
            listings = json.load(f)
            
        user_id_str = str(interaction.user.id)

        new_listing = {
            "listing_id": f"{await self.generate_listing_id(listings['listing_ids'])}",
            "item": listing_item.value,
            "user_id": interaction.user.id,
            "username": interaction.user.name,
            "listing_quantity": listing_quantity,
            "wanted_item": wanted_item.value,
            "wanted_quantity": wanted_quantity,
            "item_display_name": listing_item.name,
            "wanted_item_display_name": wanted_item.name
        }
        
            
        with open("data/listings.json", "w") as f:
            
            """
            dict is structured as follows:
            {
                "listings": {
                    "user_id": {
                        "listings":{
                            "listing_id": {Listing info}
                        }
                    }
                }
            }
            """

            if user_id_str not in listings["listings"].keys():
                listings["listings"][user_id_str] = {"listings": {}}

            listings["listings"][user_id_str]["listings"][new_listing["listing_id"]] = new_listing
            listings["listing_ids"].append(new_listing["listing_id"])
            json.dump(listings, f, indent=4)
            
            
        await interaction.response.send_message("Listing created successfully!", ephemeral=True)
        
    @app_commands.command(name = "view_listings", description = "View listings of an item")
    @app_commands.choices(listing_item = constants["item_choices"]) # NEED TO MAKE PAGINATOR
    async def view_listings(self, interaction: discord.Interaction, listing_item: app_commands.Choice[str]):
        with open("data/listings.json", "r") as f:
            listings = json.load(f)
            
        if not listings["listing_ids"]:
            await interaction.response.send_message("No listings available.", ephemeral=True)
            return
        
        embed = discord.Embed(title="Trade Listings", color=discord.Color.blue())
        
        for user_id, user_listings in listings["listings"].items():
            for listing_id, listing in user_listings["listings"].items():
                if listing["item"] == listing_item.value:
                    embed.add_field(
                        name=f"Listing ID: {listing_id}",
                        value=f"**Listed Item:** {listing['item_display_name']} **({listing['listing_quantity']}x)**\n"
                            f"**Wanted Item:** {listing['wanted_item_display_name']} **({listing['wanted_quantity']}x)**\n"
                            f"**User:** {listing['username']}",
                        inline=False
                    )
                    
        if len(embed.fields) == 0:
            await interaction.response.send_message("No listings found for this item.", ephemeral=True)
            return
                
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
        
    @app_commands.command(name = "delete_listing", description = "Delete a trade listing")
    @app_commands.autocomplete(listing_id=listings_autocomplete)
    async def delete_listing(self, interaction: discord.Interaction, listing_id: str):
        with open("data/listings.json", "r") as f:
            listings = json.load(f)
            
        user_id_str = str(interaction.user.id)
        
        if user_id_str not in listings["listings"].keys() or listing_id not in listings["listings"][user_id_str]["listings"].keys():
            await interaction.response.send_message("Listing not found.", ephemeral=True)
            return
        
        del listings["listings"][user_id_str]["listings"][listing_id]
        listings["listing_ids"].remove(listing_id)
        
        with open("data/listings.json", "w") as f:
            json.dump(listings, f, indent=4)
            
        await interaction.response.send_message(f"Listing `{listing_id}` deleted successfully!", ephemeral=True)
        
    @app_commands.command(name = "view_my_listings", description = "View your trade listings")
    async def view_my_listings(self, interaction: discord.Interaction):
        with open("data/listings.json", "r") as f:
            listings = json.load(f)
            
        user_id_str = str(interaction.user.id)
        
        if user_id_str not in listings["listings"].keys() or not listings["listings"][user_id_str]["listings"]:
            await interaction.response.send_message("You have no listings.", ephemeral=True)
            return
        
        embed = discord.Embed(title="Your Trade Listings", color=discord.Color.green())
        
        for listing_id, listing in listings["listings"][user_id_str]["listings"].items():
            embed.add_field(
                name=f"Listing ID: {listing_id}",
                value=f"**Listed Item:** {listing['item_display_name']} **({listing['listing_quantity']}x)**\n"
                    f"**Wanted Item:** {listing['wanted_item_display_name']} **({listing['wanted_quantity']}x)**",
                inline=False
            )
            
        await interaction.response.send_message(embed=embed, ephemeral=True)
        

async def setup(client):
    await client.add_cog(Trading(client))
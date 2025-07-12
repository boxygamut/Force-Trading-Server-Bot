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
        
    async def listing_item_autocomplete(self, interaction: discord.Interaction, current: str)  -> List[app_commands.Choice]:
        all_items = constants["item_choices"]
        filtered = [
            choice for choice in all_items
            if current.lower() in choice.name.lower()
        ]
        return filtered[:25]

    @app_commands.command(name = "inventory_add", description = "Create a new trade listing")
    @app_commands.autocomplete(listing_item = listing_item_autocomplete)
    @app_commands.autocomplete(wanted_item = listing_item_autocomplete)
    async def create_listing(self, interaction: discord.Interaction, listing_item: str, listing_quantity: int, wanted_item: str, wanted_quantity: int = 1):

        with open("data/listings.json", "r") as f:
            listings = json.load(f)
            
        user_id_str = str(interaction.user.id)

        new_listing = {
            "listing_id": f"{await self.generate_listing_id(listings['listing_ids'])}",
            "item": listing_item,
            "user_id": interaction.user.id,
            "username": interaction.user.name,
            "listing_quantity": listing_quantity,
            "wanted_item": wanted_item,
            "wanted_quantity": wanted_quantity,
            "item_display_name": next((choice.name for choice in constants["item_choices"] if choice.value == listing_item), "Unknown Item"),
            "wanted_item_display_name": next((choice.name for choice in constants["item_choices"] if choice.value == wanted_item), "Unknown Item")
        }
        
        if new_listing["item_display_name"] == "Unknown Item" or new_listing["wanted_item_display_name"] == "Unknown Item":
            await interaction.response.send_message("Invalid item or wanted item specified.", ephemeral=True)
            return
        
            
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

    @app_commands.command(name = "search_item", description = "View listings of an item")
    @app_commands.autocomplete(listing_item = listing_item_autocomplete)
    async def search_item(self, interaction: discord.Interaction, listing_item: str):
        with open("data/listings.json", "r") as f:
            listings = json.load(f)
            
        if not listings["listing_ids"]:
            await interaction.response.send_message("No listings available.", ephemeral=False)
            return
        
        
        
        embed_text = "```ansi\n"

        for i, (user_id, user_listings) in enumerate(listings["listings"].items()):
            for index, (listing_id, listing) in enumerate(user_listings["listings"].items()):
                if listing["item"] == listing_item:

                    embed_text += f"\u001b[0;33m[#{listing_id}] \u001b[37m{listing['item_display_name']} \u001b[2;34m({listing['listing_quantity']}x)\u001b[37m\n"
                    embed_text += f"\u001b[2;34mWanted Item\u001b[37m: {listing['wanted_item_display_name']} \u001b[2;34m({listing['wanted_quantity']}x)\n"
                    embed_text += f"\u001b[2;34mUsername\u001b[37m: {listing['username']}\n"
                    embed_text += f"\u001b[37m▬▬▬▬▬▬▬▬\n"

        embed_text = embed_text[:-14]
        embed_text += "```"
        
        embed = discord.Embed(title="Trade Listings", description = embed_text, color=discord.Color.blue())

        if len(embed.description) == 3:
            await interaction.response.send_message("No listings found for this item.", ephemeral=True)
            return

        await interaction.response.send_message(embed=embed, ephemeral=False)
        
        
    @app_commands.command(name = "inventory_delete", description = "Delete a trade listing")
    @app_commands.autocomplete(listing_id=listings_autocomplete)
    async def delete_listing(self, interaction: discord.Interaction, listing_id: str):
        with open("data/listings.json", "r") as f:
            listings = json.load(f)
            
        user_id_str = str(interaction.user.id)
        
        if user_id_str not in listings["listings"].keys() or listing_id not in listings["listings"][user_id_str]["listings"].keys():
            await interaction.response.send_message("Listing not found.", ephemeral=False)
            return
        
        del listings["listings"][user_id_str]["listings"][listing_id]
        listings["listing_ids"].remove(listing_id)
        
        with open("data/listings.json", "w") as f:
            json.dump(listings, f, indent=4)
            
        await interaction.response.send_message(f"Listing `{listing_id}` deleted successfully!", ephemeral=True)
        
    @app_commands.command(name = "inventory_view", description = "View your trade listings")
    async def view_my_listings(self, interaction: discord.Interaction):
        with open("data/listings.json", "r") as f:
            listings = json.load(f)
            
        user_id_str = str(interaction.user.id)
        
        if user_id_str not in listings["listings"].keys() or not listings["listings"][user_id_str]["listings"]:
            await interaction.response.send_message("You have no listings.", ephemeral=True)
            return
        
        
        embed_text = "```ansi\n"

        for listing_id, listing in listings["listings"][user_id_str]["listings"].items():
            embed_text += f"\u001b[0;33m[#{listing_id}] \u001b[37m{listing['item_display_name']} \u001b[2;34m({listing['listing_quantity']}x)\u001b[37m\n"
            embed_text += f"\u001b[2;34mWanted Item\u001b[37m: {listing['wanted_item_display_name']} \u001b[2;34m({listing['wanted_quantity']}x)\n"
            embed_text += f"\u001b[2;34mUsername\u001b[37m: {listing['username']}\n"
            embed_text += f"\u001b[37m▬▬▬▬▬▬▬▬\n"

        embed_text = embed_text[:-14]
        embed_text += "```"
        
        embed = discord.Embed(title="Your Trade Listings", description= embed_text, color=discord.Color.green())

        await interaction.response.send_message(embed=embed, ephemeral=False)
        
    @app_commands.command(name = "inventory_view_player", description = "View a player's trade listings")
    async def view_player_listings(self, interaction: discord.Interaction, user: discord.Member):
        with open("data/listings.json", "r") as f:
            listings = json.load(f)
            
        user_id_str = str(user.id)
        
        if user_id_str not in listings["listings"].keys() or not listings["listings"][user_id_str]["listings"]:
            await interaction.response.send_message(f"{user.mention} has no listings.", ephemeral=True)
            return
        
        embed_text = "```ansi\n"
        
        
        
        for listing_id, listing in listings["listings"][user_id_str]["listings"].items():
            embed_text += f"\u001b[0;33m[#{listing_id}] \u001b[37m{listing['item_display_name']} \u001b[2;34m({listing['listing_quantity']}x)\u001b[37m\n"
            embed_text += f"\u001b[2;34mWanted Item\u001b[37m: {listing['wanted_item_display_name']} \u001b[2;34m({listing['wanted_quantity']}x)\n"
            embed_text += f"\u001b[2;34mUsername\u001b[37m: {listing['username']}\n"
            embed_text += f"\u001b[37m▬▬▬▬▬▬▬▬\n"

        embed_text = embed_text[:-14]
        embed_text += "```"
        
        embed = discord.Embed(title=f"{user.name}'s Trade Listings", description = embed_text, color=discord.Color.purple())
        
        if len(embed_text) == 3:
            await interaction.response.send_message(f"{user.mention} has no listings.", ephemeral=True)
            return

        await interaction.response.send_message(embed=embed, ephemeral=False)
        
    
    @app_commands.command(name = "inventory_clear", description = "Delete all your trade listings")
    async def delete_all_listings(self, interaction: discord.Interaction):
        with open("data/listings.json", "r") as f:
            listings = json.load(f)
            
        user_id_str = str(interaction.user.id)
        
        if user_id_str not in listings["listings"].keys() or not listings["listings"][user_id_str]["listings"]:
            await interaction.response.send_message("You have no listings to delete.", ephemeral=True)
            return
        
        for listing_id in list(listings["listing_ids"]):
            if listing_id in listings["listings"][user_id_str]["listings"]:
                listings["listing_ids"].remove(listing_id)
        
        listings["listings"][user_id_str]["listings"] = {}
        
        
        with open("data/listings.json", "w") as f:
            json.dump(listings, f, indent=4)
            
        await interaction.response.send_message("All your listings have been deleted.", ephemeral=True)
        
        
    @app_commands.command(name = "set_desired_items", description = "Add items you want to trade for")
    async def set_wanted_items(self, interaction: discord.Interaction, items: str):
        
        with open("data/listings.json", "r") as f:
            data = json.load(f)
            
        if not str(interaction.user.id) in data["listings"].keys():
            data["listings"][str(interaction.user.id)] = {"listings": {}, "desired_items": "", "available_items": ""}

        data["listings"][str(interaction.user.id)]["desired_items"] = items

        with open("data/listings.json", "w") as f:
            json.dump(data, f, indent=4)

        await interaction.response.send_message("Your desired items have been updated.", ephemeral=True)
        
    @app_commands.command(name = "clear_desired_items", description = "Clear your desired items")
    async def clear_desired_items(self, interaction: discord.Interaction):
        with open("data/listings.json", "r") as f:
            data = json.load(f)
            
        if str(interaction.user.id) in data["listings"]:
            del data["listings"][str(interaction.user.id)]["desired_items"]
            with open("data/listings.json", "w") as f:
                json.dump(data, f, indent=4)
                
            await interaction.response.send_message("Your desired items have been cleared.", ephemeral=True)
        else:
            await interaction.response.send_message("You have no desired items to clear.", ephemeral=True)
            
    @app_commands.command(name = "set_available_items", description = "Add items you have available for trade")
    async def set_available_items(self, interaction: discord.Interaction, items: str):
        with open("data/listings.json", "r") as f:
            data = json.load(f)
            
        if not str(interaction.user.id) in data["listings"].keys():
            data["listings"][str(interaction.user.id)] = {"listings": {}, "available_items": "", "desired_items": ""}

        data["listings"][str(interaction.user.id)]["available_items"] = items

        with open("data/listings.json", "w") as f:
            json.dump(data, f, indent=4)

        await interaction.response.send_message("Your available items have been updated.", ephemeral=True)
        
    @app_commands.command(name = "clear_available_items", description = "Clear your available items")
    async def clear_available_items(self, interaction: discord.Interaction):
        with open("data/listings.json", "r") as f:
            data = json.load(f)
            
        if str(interaction.user.id) in data["listings"].keys():
            del data["listings"][str(interaction.user.id)]["available_items"]
            with open("data/listings.json", "w") as f:
                json.dump(data, f, indent=4)
                
            await interaction.response.send_message("Your available items have been cleared.", ephemeral=True)
        else:
            await interaction.response.send_message("You have no available items to clear.", ephemeral=True)
            
    @app_commands.command(name = "view_player", description = "View player's desired and wanted items")
    async def view_player(self, interaction: discord.Interaction, user: discord.Member):
        with open("data/listings.json", "r") as f:
            data = json.load(f)
            
        user_id_str = str(user.id)

        if user_id_str not in data["listings"]:
            await interaction.response.send_message(f"{user.mention} does not have any desired or available items.", ephemeral=True)
            return
        
        
        if "desired_items" not in data["listings"][user_id_str].keys():
            desired_items = "None"
        
        else:
            desired_items = data["listings"][user_id_str]["desired_items"]
            
        if "available_items" not in data["listings"][user_id_str].keys():
            available_items = "None"
        
        else:
            available_items = data["listings"][user_id_str]["available_items"]
            
        embed_text = "```ansi\n"

        embed_text += f"\u001b[2;34mDesired items: \u001b[37m{desired_items}\n"
        embed_text += f"\u001b[2;34mAvailable items: \u001b[37m{available_items}\n"
        embed_text += "```"

        embed = discord.Embed(title=f"{user.name}'s Trade Preferences", description=embed_text, color=discord.Color.blue())

        await interaction.response.send_message(embed=embed, ephemeral=False)

async def setup(client):
    await client.add_cog(Trading(client))
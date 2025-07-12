import discord
from discord import app_commands

constants = {
    "item_choices":[
            app_commands.Choice(name="Durasteel Bar", value="durasteel_bar"),
            app_commands.Choice(name="Beskar Bar", value="beskar_bar"),
            app_commands.Choice(name="Forge Schematic", value="forge_schematic"),
            app_commands.Choice(name="Brylack Log", value="brylack_log"),
            app_commands.Choice(name="None", value="None"),
            app_commands.Choice(name="Looking for Offers", value="looking_for_offers"),
            
            # Obi-wan Set
            app_commands.Choice(name="Obi-wan Set", value="obi_wan_set"),
            app_commands.Choice(name="Obi-wan Pommel", value="obi_wan_pommel"),
            app_commands.Choice(name="Obi-wan Emitter", value="obi_wan_emitter"),
            app_commands.Choice(name="Obi-wan Sleeve", value="obi_wan_sleeve"),

            # Ronin Set
            app_commands.Choice(name="Ronin Set", value="ronin_set"),
            app_commands.Choice(name="Ronin Pommel", value="ronin_pommel"),
            app_commands.Choice(name="Ronin Emitter", value="ronin_emitter"),
            app_commands.Choice(name="Ronin Sleeve", value="ronin_sleeve"),

            # Vahlken Set
            app_commands.Choice(name="Vahlken Set", value="vahlken_set"),
            app_commands.Choice(name="Vahlken Pommel", value="vahlken_pommel"),
            app_commands.Choice(name="Vahlken Emitter", value="vahlken_emitter"),
            app_commands.Choice(name="Vahlken Sleeve", value="vahlken_sleeve"),

            # Krayt Set
            app_commands.Choice(name="Krayt Set", value="krayt_set"),
            app_commands.Choice(name="Krayt Pommel", value="krayt_pommel"),
            app_commands.Choice(name="Krayt Emitter", value="krayt_emitter"),
            app_commands.Choice(name="Krayt Sleeve", value="krayt_sleeve"),

            # Rey Set
            app_commands.Choice(name="Rey Set", value="rey_set"),
            app_commands.Choice(name="Rey Pommel", value="rey_pommel"),
            app_commands.Choice(name="Rey Emitter", value="rey_emitter"),
            app_commands.Choice(name="Rey Sleeve", value="rey_sleeve"),

            # Revenge Set
            app_commands.Choice(name="Revenge Set", value="revenge_set"),
            app_commands.Choice(name="Revenge Pommel", value="revenge_pommel"),
            app_commands.Choice(name="Revenge Emitter", value="revenge_emitter"),
            app_commands.Choice(name="Revenge Sleeve", value="revenge_sleeve"),

            # Synthetic Set
            app_commands.Choice(name="Synthetic Set", value="synthetic_set"),
            app_commands.Choice(name="Synthetic Pommel", value="synthetic_pommel"),
            app_commands.Choice(name="Synthetic Emitter", value="synthetic_emitter"),
            app_commands.Choice(name="Synthetic Sleeve", value="synthetic_sleeve"),

            # Beowulf Set
            app_commands.Choice(name="Beowulf Set", value="beowulf_set"),
            app_commands.Choice(name="Beowulf Pommel", value="beowulf_pommel"),
            app_commands.Choice(name="Beowulf Emitter", value="beowulf_emitter"),
            app_commands.Choice(name="Beowulf Sleeve", value="beowulf_sleeve"),

            # Peralun Set
            app_commands.Choice(name="Peralun Set", value="peralun_set"),
            app_commands.Choice(name="Peralun Pommel", value="peralun_pommel"),
            app_commands.Choice(name="Peralun Emitter", value="peralun_emitter"),
            app_commands.Choice(name="Peralun Sleeve", value="peralun_sleeve"),

            # Malgus Set
            app_commands.Choice(name="Malgus Set", value="malgus_set"),
            app_commands.Choice(name="Malgus Pommel", value="malgus_pommel"),
            app_commands.Choice(name="Malgus Emitter", value="malgus_emitter"),
            app_commands.Choice(name="Malgus Sleeve", value="malgus_sleeve"),

            # Inquisitor Set
            app_commands.Choice(name="Inquisitor Set", value="inquisitor_set"),
            app_commands.Choice(name="Inquisitor Pommel", value="inquisitor_pommel"),
            app_commands.Choice(name="Inquisitor Emitter", value="inquisitor_emitter"),
            app_commands.Choice(name="Inquisitor Sleeve", value="inquisitor_sleeve"),

            # Zil Set
            app_commands.Choice(name="Zil Set", value="zil_set"),
            app_commands.Choice(name="Zil Pommel", value="zil_pommel"),
            app_commands.Choice(name="Zil Emitter", value="zil_emitter"),
            app_commands.Choice(name="Zil Sleeve", value="zil_sleeve"),

            # Kestis Set
            app_commands.Choice(name="Kestis Set", value="kestis_set"),
            app_commands.Choice(name="Kestis Pommel", value="kestis_pommel"),
            app_commands.Choice(name="Kestis Emitter", value="kestis_emitter"),
            app_commands.Choice(name="Kestis Sleeve", value="kestis_sleeve"),

            # Crossguard Set
            app_commands.Choice(name="Crossguard Set", value="crossguard_set"),
            app_commands.Choice(name="Crossguard Pommel", value="crossguard_pommel"),
            app_commands.Choice(name="Crossguard Emitter", value="crossguard_emitter"),
            app_commands.Choice(name="Crossguard Sleeve", value="crossguard_sleeve"),

            # Fallsaber Set
            app_commands.Choice(name="Fallsaber Set", value="fallsaber_set"),
            app_commands.Choice(name="Fallsaber Pommel", value="fallsaber_pommel"),
            app_commands.Choice(name="Fallsaber Emitter", value="fallsaber_emitter"),
            app_commands.Choice(name="Fallsaber Sleeve", value="fallsaber_sleeve"),

            # Knight Set
            app_commands.Choice(name="Knight Set", value="knight_set"),
            app_commands.Choice(name="Knight Pommel", value="knight_pommel"),
            app_commands.Choice(name="Knight Emitter", value="knight_emitter"),
            app_commands.Choice(name="Knight Sleeve", value="knight_sleeve"),
            
            #Overall "Stuff"
            app_commands.Choice(name = "Knight Stuff", value = "knight_stuff"),
            app_commands.Choice(name = "Fall Saber Stuff", value = "fallsaber_stuff"),
            app_commands.Choice(name = "Crossguard Stuff", value = "crossguard_stuff"),
            app_commands.Choice(name = "Kestis Stuff", value = "kestis_stuff"),
            app_commands.Choice(name = "Zil Stuff", value = "zil_stuff"),
            app_commands.Choice(name = "Inquisitor Stuff", value = "inquisitor_stuff"),
            app_commands.Choice(name = "Malgus Stuff", value = "malgus_stuff"),
            app_commands.Choice(name = "Peralun Stuff", value = "peralun_stuff"),
            app_commands.Choice(name = "Beowulf Stuff", value = "beowulf_stuff"),
            app_commands.Choice(name = "Synthetic Stuff", value = "synthetic_stuff"),
            app_commands.Choice(name = "Revenge Stuff", value = "revenge_stuff"),
            app_commands.Choice(name = "Rey Stuff", value = "rey_stuff"),
            app_commands.Choice(name = "Krayt Stuff", value = "krayt_stuff"),
            app_commands.Choice(name = "Vahlken Stuff", value = "vahlken_stuff"),
            app_commands.Choice(name = "Ronin Stuff", value = "ronin_stuff"),
            app_commands.Choice(name = "Obi-wan Stuff", value = "obi_wan_stuff")

    ],
    "item_choices_raw": [
            "durasteel_bar",
            "beskar_bar",
            "forge_schematic",
            "brylack_log",
            "obi_wan_set",
            "obi_wan_pommel",
            "obi_wan_emitter",
            "obi_wan_sleeve",
            "ronin_set",
            "ronin_pommel",
            "ronin_emitter",
            "ronin_sleeve",
            "vahlken_set",
            "vahlken_pommel",
            "vahlken_emitter",
            "vahlken_sleeve",
            "krayt_set",
            "krayt_pommel",
            "krayt_emitter",
            "krayt_sleeve",
            "rey_set",
            "rey_pommel",
            "rey_emitter",
            "rey_sleeve",
            "revenge_set",
            "revenge_pommel",
            "revenge_emitter",
            "revenge_sleeve",
            "synthetic_set",
            "synthetic_pommel",
            "synthetic_emitter",
            "synthetic_sleeve",
            "beowulf_set",
            "beowulf_pommel",
            "beowulf_emitter",
            "beowulf_sleeve",
            "peralun_set",
            "peralun_pommel",
            "peralun_emitter",
            "peralun_sleeve",
            "malgus_set",
            "malgus_pommel",
            "malgus_emitter",
            "malgus_sleeve",
            "inquisitor_set",
            "inquisitor_pommel",
            "inquisitor_emitter",
            "inquisitor_sleeve",
            "zil_set",
            "zil_pommel",
            "zil_emitter",
            "zil_sleeve",
            "kestis_set",
            "kestis_pommel",
            "kestis_emitter",
            "kestis_sleeve",
            "crossguard_set",
            "crossguard_pommel",
            "crossguard_emitter",
            "crossguard_sleeve",
            "fallsaber_set",
            "fallsaber_pommel",
            "fallsaber_emitter",
            "fallsaber_sleeve",
            "knight_set",
            "knight_pommel",
            "knight_emitter",
            "knight_sleeve"
    ],
}
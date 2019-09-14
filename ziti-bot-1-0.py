# Ziti Bot v1.0, a melding of XIVAPI.py and Discord.py
#  to allow for queries in the Discord overlay

# Discord bot engine
import discord
from discord.ext import commands
# Dependancies for xivapi
import asyncio
import logging
import aiohttp
# XIVAPI engine
import xivapi

# XIVAPI initializing
x_key = "xivapi-api-key-here"

# Discord bot initializing
ziti = commands.Bot(command_prefix = 'z.')
@ziti.event
async def on_ready():
    print("Ziti Bot is now online.")

# Ask Ziti Bot what it can do for me?
# "z.commands" or "z.list" or "z.help"
@ziti.command(aliases=['commands', 'list'])
async def commandList(ctx):
    await ctx.send("Ziti Bot is online!\nAvailable Commands: z.getid, z.item, z.recipe, z.help")


@ziti.command()
async def getid(ctx, *, inquiry):
    ''' Search for an item by (partial/full)name. Returns ID #'s '''
#    logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='%H:%M')
    x_session = aiohttp.ClientSession()
    x_client = xivapi.Client(session=x_session, api_key=x_key)
    results = await x_client.index_search(
        name=f"{inquiry}",
        indexes=["Item"],
        columns=["Name","ID","GameContentLinks.Recipe.ItemResult.0"]
        )
    output = ''
    for each in results['Results']:
        output = output + f"{each['Name']}: ID {each['ID']}, Recipe {each['GameContentLinks']['Recipe']['ItemResult']}\n"
    await ctx.send(output)

@ziti.command()
async def item(ctx, *, inquiry):
    ''' Use the Item ID to get a description of that item. '''
#    logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='%H:%M')
    x_session = aiohttp.ClientSession()
    x_client = xivapi.Client(session=x_session, api_key=x_key)
    results = await x_client.index_by_id(
        index="Item", 
        content_id=f"{inquiry}", 
        columns=["Name","ID","Description","ItemUICategory.Name"]
        )
    output = f"ID {results['ID']}, {results['Name']}: {results['ItemUICategory']['Name']}\n{results['Description']}"
    await ctx.send(output)

@ziti.command()
async def recipe(ctx, *, inquiry):
    ''' Use the Recipe ID to get the requirements for crafting. '''
#    logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='%H:%M')
    x_session = aiohttp.ClientSession()
    x_client = xivapi.Client(session=x_session, api_key=x_key)
    results = await x_client.index_by_id(
        index="Recipe", 
        content_id=f"{inquiry}", 
        columns=["Name","ID",
            "ItemIngredient0.Name","AmountIngredient0",
            "ItemIngredient1.Name","AmountIngredient1",
            "ItemIngredient2.Name","AmountIngredient2",
            "ItemIngredient3.Name","AmountIngredient3",
            "ItemIngredient4.Name","AmountIngredient4",
            "ItemIngredient5.Name","AmountIngredient5",
            "ItemIngredient6.Name","AmountIngredient6",
            "ItemIngredient7.Name","AmountIngredient7",
            "ItemIngredient8.Name","AmountIngredient8",
            "ItemIngredient9.Name","AmountIngredient9",
            "ClassJob.Abbreviation", "RecipeLevelTable.ClassJobLevel"
            ]
        )
    resultlist = list(results)
    ingredients = ''
    for each in range(10):
        if results[resultlist[each]] > 0:
            ingredients = ingredients + f"{results[resultlist[each+12]]['Name']} x {results[resultlist[each]]}\n"
    output = f"\nRecipe {results['ID']}: {results['Name']}, {results['ClassJob']['Abbreviation']} lvl {results['RecipeLevelTable']['ClassJobLevel']}\n{ingredients}"
    await ctx.send(output)


## This code starts up the script
# and connects it to your Discord App bot
ziti.run('discord-bot-token-here')

## Ziti Bot - stable v1.2 - by Angadeon

import re
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
x_key = "your-xivapi-key-here"

# Discord bot initializing
ziti = commands.Bot(command_prefix = 'z.')
@ziti.event
async def on_ready():
    print("Ziti Bot is now online.")

# Ask Ziti Bot what it can do for me?
# "z.commands" or "z.list" or "z.help"
@ziti.command(aliases=['commands', 'list'])
async def commandList(ctx):
    await ctx.send("Ziti bot is online!\nAvailable Commands: z.getid, z.item, z.recipe, z.help")

@ziti.command()
async def item(ctx, *, inquiry):
    ''' Search for an item by (partial)name.'''
#    logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='%H:%M')
    x_session = aiohttp.ClientSession()
    x_client = xivapi.Client(session=x_session, api_key=x_key)
    results = await x_client.index_search(
        name=f"{inquiry}",
        indexes=["Item"],
        columns=["Name",
        "Description",
        "ItemKind.Name",
        "ItemUICategory.Name"]
        )
    output = '\n'
    for each in results['Results']:
        output = output + f"{each['Name']}: " + re.sub(r'\n+', r' ', each['Description']) + f", {each['ItemKind']['Name']} - {each['ItemUICategory']['Name']}\n\n"
    await ctx.send(output)

@ziti.command()
async def recipe(ctx, *, inquiry):
    ''' Displays the ingredients and amounts needed for crafting an item. '''
#    logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='%H:%M')
    x_session = aiohttp.ClientSession()
    x_client = xivapi.Client(session=x_session, api_key=x_key)
    results = await x_client.index_search(
        name=f"{inquiry}",
        indexes=["Recipe"],
        string_algo="match_phrase",
        columns=["Name",
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
#    print(results)
    if results['Pagination']['Results'] == 0:
        await ctx.send("This recipe does not appear to exist as named.")
    else:
        resultB = results['Results'][0]
        resultlist = list(resultB)
        ingredients = ''
        for each in range(10):
            if resultB[resultlist[each]] > 0:
                ingredients = ingredients + f"{resultB[resultlist[each+11]]['Name']} x {resultB[resultlist[each]]}\n"
        output = f"\nRecipe: {resultB['Name']}, {resultB['ClassJob']['Abbreviation']}, lvl {resultB['RecipeLevelTable']['ClassJobLevel']}\n{ingredients}"
        await ctx.send(output)

## This code starts up the bot
# and gives it access to the specific Discord channel
ziti.run('your-discord-bot-token-here')
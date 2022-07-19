#Imports and load dotenv
import os
import discord
from discord.ext import commands
#from dotenv import load_dotenv
from espn import *
from nbaapi import *
#load_dotenv()

#Initialize Client
client = discord.Client()
TOKEN = os.getenv('TOKEN')
bot = commands.Bot(command_prefix="$")

#Debug - Bot Start
@client.event
async def on_ready():
    print("Logged in as {0.user}.".format(client))

#Hello World Function
@client.event
async def on_message(message):
    #Ignore message if it is sent by the bot
    if message.author == client.user:
        return
    
    #Free Agents Command
    if message.content.startswith("/freeagents"):
        await message.channel.send("Which Position? (PG / SG / SF / PF / C / G / F)\n")
        def check(mes):
            return mes.content in ['PG','SG','SF','PF','C','G','F'] and mes.channel == message.channel and mes.author == message.author  
        msg = await client.wait_for('message',check=check)
        answer = free_agents(5, str(msg.content))
        await message.channel.send(answer)
    
    #Teams Command
    if message.content.startswith("/teams"):
        answer = print_teams()
        await message.channel.send(answer)
    
    #Matchups Command
    if message.content.startswith("/matchups"):
        answer = matchup()
        await message.channel.send(answer)
    
    #Roster Command
    if message.content.startswith("/teaminfo"):
        await message.channel.send("Which team would you like to view the roster for? (Respond with number)")
        answer = print_teams()
        await message.channel.send(answer)
        def check(mes):
            return 1 <= int(str(mes.content)) <= get_team_number()
        msg = await client.wait_for('message', check=check)
        answer2 = team_info(int(str(msg.content)))
        await message.channel.send(answer2)
    
    #Player Stats Command
    if message.content.startswith("/playerstats"):
        value = message.content.split("/playerstats ",1)[1]
        print(value)
        #await message.channel.send(value)
        response = get_season_stats(value)
        await message.channel.send(response)

    #Estimated Stats Command
    if message.content.startswith("/estimatedstats"):
        value = message.content.split("/estimatedstats ",1)[1]
        print(value)
        response = estimated_metrics(value)
        await message.channel.send(response)

    #Estimated Team Stats Command:
    if message.content.startswith("/estimatedteamstats"):
        value = message.content.split("/estimatedteamstats ",1)[1]
        print(value)
        response = team_estimated_metrics(value)
        await message.channel.send(response)
    
    #Hustle Stats Command:
    if message.content.startswith("/hustlestats"):
        await message.channel.send("""
    Which Hustle Stat would you like to view the leaders for? (Reply with Number)
    1. Charges Drawn
    2. Contested Shots
    3. Deflections
    4. Loose Balls
    5. Screen Assists
    """)
        def check(mes):
            return 1<=int(str(mes.content))<=5 and mes.channel == message.channel and mes.author == message.author
        msg = await client.wait_for('message',check=check)
        answer = hustle_stats_leaders(stat_choice=(int(str(msg.content))))
        await message.channel.send(answer)

    #Activity Command:
    if message.content.startswith("/activity"):
        response = activity()
        await message.channel.send(response)

    #Matchup Data Command
    if message.content.startswith("/playermatchups"):
        temp = message.content.strip("/playermatchups ")
        temp = temp.split(',')
        answer = matchup_data(temp[0],temp[1])
        await message.channel.send(answer)
        print(temp)
# @bot.command()
# async def playerstats(ctx, *, arg):
#     response = get_season_stats(arg)
#     await ctx.send(arg)
#     await ctx.send(response)

client.run(TOKEN)
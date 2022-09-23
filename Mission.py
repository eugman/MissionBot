#!/usr/bin/env python3

def contains(message, commands):
    for command in commands:
        if command in message.content.lower():
            return True

def equals(message, commands):
    for command in commands:
        if command == message.content:
            return True

def command(message, command):
    if message.content.lower().startswith('!' + command): 
        return True



import discord
import random
import socket
import asyncio
import os.path
import pickle


missions = ["Acquisition", "Annihilation", "Biotechvore", "Capture and Protect", 
        "Countermeasures", "Decapitation", "Firefight", "Frostbyte", 
        "Frontline", "Highly Classified", "Looting and Sabotage", "Mindwipe", 
        "Panic Room", "Power Pack", "Quadrant Control", "Rescue", 
        "Supplies", "Supremacy", "The Armory", "Unmasking", 
        "Non-standard ITS mission", "Narrative Mission"]

narrativeMissions = []

client = discord.Client()
client.mission = "Unknown mission"
client.prevMissions = [11, 4, 2, 11]

if os.path.exists('save.p'):
    client.mission, client.prevMissions = pickle.load(open("save.p", "rb"))

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(client.mission))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if command(message, "random"):
        
        if message.author.name == "metalface13":
            await message.channel.send("I can't let you do that, Casey")
            return
            

        missionID = client.prevMissions[0]
        while missionID in client.prevMissions:
            missionID = random.randint(0,21)
            print(missionID)
            print("New mission: " + missions[missionID])

        client.prevMissions = client.prevMissions[1:] + [missionID]
        client.mission = missions[missionID]
        await client.change_presence(activity=discord.Game(client.mission))

        pickle.dump([client.mission, client.prevMissions], open("save.p", "wb"))
        await message.channel.send("You are playing " + client.mission )
    
    if command(message, "mission"):
        await message.channel.send("You are playing " + client.mission )
    
    if command(message, "previous"):
        await message.channel.send("Previous missions were " + ", ".join([missions[x] for x in client.prevMissions]))

    
    if command(message, "help"):
        await message.channel.send("Commands are\n**!random** will generate a new mission\n**!mission** will show the current mission\n**!previous** will show the previous missions\n**!help** will display this message" )
    
client.run(open("apikey.txt",'r').read().strip())

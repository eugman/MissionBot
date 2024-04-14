#/usr/bin/env python3

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
#
import json
#

missionData = open("MissionParams.json")

missions = json.load(missionData)
missionList = list(missions)

'''
Missiondata structure:
MissionName:{
    description: (str) # brief description of mission
    hvt: (int) # number of HVTs per player
    classifieds: (int) # number of classified objectives per player
    seasonrules: (list[str]) # list containing strings of seasonal modifiers
'''

#I think I remember that there's a cuter way to do file IO, but I'm rusty as hell - LL
missionData.close()
'''
missions = ["Acquisition", "B-pong", "Biotechvore", "Capture and Protect", 
        "Countermeasures", "Decapitation", "Evacuation", "Firefight",
        "Frostbyte", "Frontline", "Highly Classified", "Last Launch", 
        "Looting and Sabotage", "Mindwipe", "Panic Room", "Power Pack", 
        "Supplies", "Supremacy", "The Armory", "Unmasking", 
        "Direct Action Mission", "Narrative Mission"]
missionSummary = ["Activate the antennas, control the antennas, control the tech coffin"]

narrativeMissions = []
'''






client = discord.Client(intents=discord.Intents.default())
client.currentMission = "Acquisition"
client.missionData = missions[client.currentMission]
client.prevMissions = [1, 1, 1, 1]


if os.path.exists('save.p'):
    client.currentMission, client.prevMissions = pickle.load(open("save.p", "rb"))

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(client.currentMission))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if command(message, "random"):
        
        if message.author.name == "metalface13":
            await message.channel.send("I can't let you do that, Casey")
            return
            
#Todo: refactor code s.t. you're pulling from new mission data
# Option: do the list-ening of the dict outside the loop for computational efficiency
        missionID = client.prevMissions[0]

        while missionID in client.prevMissions:
            missionID = random.randint(0,len(missions))
            print(missionID)
            print("New mission: " + missionList[missionID])

        client.prevMissions = client.prevMissions[1:] + [missionID]

        client.currentMission = missionList[missionID]
        client.missionData = missions[client.currentMission]

        await client.change_presence(activity=discord.Game(client.currentMission))

        pickle.dump([client.currentMission, client.prevMissions], open("save.p", "wb"))
        await message.channel.send("You are playing " + client.currentMission )
        await message.channel.send("Description: " + client.missionData["description"] )
    
    if command(message, "mission"):
        await message.channel.send("You are playing " + client.currentMission )
        await message.channel.send("Description: " + client.missionData["description"] )
    
    if command(message, "previous"):
        await message.channel.send("Previous missions were " + ", ".join([missionList[x] for x in client.prevMissions]))

    if command(message, "list"):
        allMissions = ""
        for i in range(len(missions)):
            allMissions += str(i+1) + " - " + missionList[i] + "\n"
        await message.channel.send("All missions:\n " + allMissions)
    
    if command(message, "set"):
        missionID = int(message.content.split()[-1])-1
        client.prevMissions = client.prevMissions[1:] + [missionID]
        client.currentMission = missionList[missionID]
        await client.change_presence(activity=discord.Game(client.currentMission))

        pickle.dump([client.currentMission, client.prevMissions], open("save.p", "wb"))
        await message.channel.send("You are playing " + client.currentMission )
        await message.channel.send("Description: " + client.missionData["description"] )
        if client.missionData["reinforcements"] and random.randint(0, 4) == 0:
            await message.channel.send("Description: " + client.missionData["description"] )
    

    if command(message, "help"):
        await message.channel.send("Commands are\n**!random** will generate a new mission\n**!mission** will show the current mission\n**!previous** will show the previous missions\n**!list** will show all missions\n**!set** takes the mission number in !list to set to specified mission\n**!help** will display this message" )
    
client.run(open("apikey.txt",'r').read().strip())

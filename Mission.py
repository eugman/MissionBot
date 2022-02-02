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


#if os.path.exists('save.p'):
#    game = pickle.load(open("save.p", "rb"))
#else:
#    game = Game()


missions = ["Aqcuisition", "Annihilation", "Biotechvore", "Capture and Protect", "Countermeasures", "Decapitation", "Firefight", "Frostbyte", "Frontline", "Highly Classified", "Looting and Sabotage", "Mindwipe", "Panic Room", "Power Pack" "Quadrant Control", "Rescue", "Supplies", "Supremacy", "The Armory", "Unmasking"]

client = discord.Client()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if command(message, "random"):
        await message.channel.send("You are playing " + missions[random.randint(0,19)])


client.run(open("apikey.txt",'r').read().strip())

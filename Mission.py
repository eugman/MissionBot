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
import os
import os.path
import pickle
import datetime
from zoneinfo import ZoneInfo
from discord.ext import tasks
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

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

client.currentMission = missionList[0]
client.prevMissions = [1, 1, 1, 1]


if os.path.exists('save.p'):
    try:
        with open("save.p", "rb") as f:
            savedMission, savedPrev = pickle.load(f)
        # Only honor the saved mission if it still exists in the current
        # MissionParams.json. Mission names change between ITS seasons, so a
        # stale save.p (or stale default) must not crash the bot on startup.
        if savedMission in missions:
            client.currentMission = savedMission
        # Drop saved mission indices that are out of range for the current
        # mission list (it shrinks between seasons), then pad back to 4 so the
        # dedup window and the !previous command can never IndexError.
        validPrev = [i for i in savedPrev if isinstance(i, int) and 0 <= i < len(missions)]
        client.prevMissions = (validPrev + [0, 0, 0, 0])[:4]
    except Exception as exc:
        # A corrupt / truncated / legacy save.p must never crash startup — that
        # was the original failure mode. Fall back to defaults.
        print(f"Could not read save.p ({exc!r}); starting from defaults.")
        client.currentMission = missionList[0]
        client.prevMissions = [1, 1, 1, 1]

client.missionData = missions[client.currentMission]


def pick_new_mission():
    """Roll a new random mission, avoiding the most recent ones, and persist state.

    Updates client.currentMission / client.missionData / client.prevMissions and
    writes save.p. Callers handle presence updates and any channel messages.
    """
    missionID = client.prevMissions[0]
    while missionID in client.prevMissions:
        missionID = random.randrange(len(missions))
    client.prevMissions = client.prevMissions[1:] + [missionID]
    client.currentMission = missionList[missionID]
    client.missionData = missions[client.currentMission]
    save_state()


def save_state():
    """Persist current mission + recent-mission window to save.p."""
    with open("save.p", "wb") as f:
        pickle.dump([client.currentMission, client.prevMissions], f)


# --- Weekly auto-post configuration ---
# Posts a fresh random mission to the channel given by MISSION_CHANNEL_ID once a
# week. The ID is read from the environment (see .env, loaded by systemd via
# EnvironmentFile). There is no fallback: if MISSION_CHANNEL_ID is not set, the
# weekly post is simply never scheduled (see on_ready).
_raw_channel_id = os.environ.get("MISSION_CHANNEL_ID", "").strip()
try:
    # No fallback: unset/empty disables the weekly post. A malformed value also
    # disables it (rather than crashing at import, which under systemd's
    # Restart=always would become a crash loop).
    WEEKLY_CHANNEL_ID = int(_raw_channel_id) if _raw_channel_id else None
except ValueError:
    print(f"MISSION_CHANNEL_ID={_raw_channel_id!r} is not a valid integer — weekly post disabled.")
    WEEKLY_CHANNEL_ID = None
WEEKLY_POST_WEEKDAY = 6                      # Monday=0 ... Sunday=6
WEEKLY_POST_TIME = datetime.time(hour=17, minute=0, tzinfo=ZoneInfo("America/New_York"))  # Pittsburgh time (5 PM)


@tasks.loop(time=WEEKLY_POST_TIME)
async def weekly_mission_post():
    # tasks.loop(time=...) fires daily at WEEKLY_POST_TIME; only act on the target weekday.
    if datetime.datetime.now(WEEKLY_POST_TIME.tzinfo).weekday() != WEEKLY_POST_WEEKDAY:
        return
    # Never let an exception escape this coroutine: an unhandled error would stop
    # the loop permanently (no further weekly posts until the service restarts).
    try:
        channel = client.get_channel(WEEKLY_CHANNEL_ID)
        if channel is None:
            print(f"weekly_mission_post: channel {WEEKLY_CHANNEL_ID} not found (bot not in guild, or cache not ready)")
            return
        pick_new_mission()
        await client.change_presence(activity=discord.Game(client.currentMission))
        await channel.send("🎲 **This week's mission: " + client.currentMission + "**")
        await channel.send("Description: " + client.missionData["description"])
    except Exception as exc:
        print(f"weekly_mission_post failed: {exc!r}")


@weekly_mission_post.before_loop
async def before_weekly_mission_post():
    # Wait until the gateway is connected and guild/channel caches are populated.
    await client.wait_until_ready()


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(client.currentMission))
    if WEEKLY_CHANNEL_ID is None:
        print("MISSION_CHANNEL_ID not set in environment — weekly mission post is disabled.")
    elif not weekly_mission_post.is_running():
        weekly_mission_post.start()

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if command(message, "random"):
        pick_new_mission()
        await client.change_presence(activity=discord.Game(client.currentMission))
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
        parts = message.content.split()
        if len(parts) < 2 or not parts[-1].lstrip('-').isdigit():
            await message.channel.send("Usage: !set <mission number from !list>")
            return
        missionID = int(parts[-1]) - 1
        if not (0 <= missionID < len(missions)):
            await message.channel.send(f"Invalid mission number. Use 1-{len(missions)} (see !list).")
            return
        client.prevMissions = client.prevMissions[1:] + [missionID]
        client.currentMission = missionList[missionID]
        client.missionData = missions[client.currentMission]
        await client.change_presence(activity=discord.Game(client.currentMission))
        save_state()
        await message.channel.send("You are playing " + client.currentMission )
        await message.channel.send("Description: " + client.missionData["description"] )
    

    if command(message, "help"):
        await message.channel.send("Commands are\n**!random** will generate a new mission\n**!mission** will show the current mission\n**!previous** will show the previous missions\n**!list** will show all missions\n**!set** takes the mission number in !list to set to specified mission\n**!help** will display this message" )
    
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN", "").strip()
if not DISCORD_TOKEN:
    raise SystemExit("DISCORD_TOKEN is not set in the environment (see .env / EnvironmentFile). Cannot start.")
client.run(DISCORD_TOKEN)

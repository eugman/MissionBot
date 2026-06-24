# MissionBot
Really simple Discord bot for posting weekly missions for the Infinity Miniatures game.

# Requirements
Requires discord.py installed and Python3.

Configuration comes from environment variables (see `.env.sample`). Copy it to
`.env` and fill in:
- `DISCORD_TOKEN` (required) — the bot token. The bot exits at startup if unset.
- `MISSION_CHANNEL_ID` (optional) — channel for the weekly auto-post; if unset,
  the weekly post is simply not scheduled.

On the Raspberry Pi the `.env` is loaded by systemd via
`EnvironmentFile=-/home/pi/MissionBot/.env` in `discordbot.service`.

To install dicord.py run the following:
```
python3 -m pip install -U discord.py
```

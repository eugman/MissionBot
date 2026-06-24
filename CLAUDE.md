# MissionBot

Discord bot for the Infinity miniatures game (ITS). Players pick/announce
missions via `!` commands, and the bot auto-posts a random mission once a week
(Sundays 5 PM America/New_York) to the channel in `MISSION_CHANNEL_ID`.

## Layout

- `Mission.py` — the entire bot (discord.py 2.x): `!` commands + the weekly
  `tasks.loop`. Shared mission selection lives in `pick_new_mission()`.
- `MissionParams.json` — mission data. Values (`hvt`, `classifieds`,
  `reinforcements`, `seasonrules`) must match the current official ITS rulebook.
- `save.p` — pickled runtime state (`[currentMission, prevMissions]`). Gitignored,
  recreated at runtime; safe to delete to reset. Never crashes startup if stale.

## Config & secrets

- Config is via environment variables: `DISCORD_TOKEN` (required; bot exits if
  unset) and `MISSION_CHANNEL_ID` (optional; disables the weekly post if unset).
- Secrets live only in `.env` (gitignored, loaded by systemd `EnvironmentFile=`).
  Never commit `.env`, the token, or the channel ID — channel IDs in a public repo
  invite spam bots.

## Deploy

Runs as a systemd service on a Raspberry Pi. Deploy = push to `main`, then pull
on the Pi. Setup / redeploy / verify steps: see `INSTALL.md`.

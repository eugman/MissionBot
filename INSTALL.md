# MissionBot — Install & Deploy

The bot runs on a Raspberry Pi as a systemd service (`discordbot.service`,
running as root). The canonical unit file lives in this repo and is installed to
`/etc/systemd/system/`. Deploy model: push to `main`, then pull on the Pi.

**SSH into the Pi first**, then run the commands below from the machine (they
assume an interactive session and that the repo is at `~/MissionBot`).

## Configuration

Config comes from environment variables (see `.env.sample`). Copy it to `.env`
(gitignored) and fill in:

- `DISCORD_TOKEN` (required) — the bot token. The bot exits at startup if unset.
- `MISSION_CHANNEL_ID` (optional) — channel for the weekly auto-post. If unset,
  the weekly post is not scheduled; all `!` commands still work.

The `.env` is loaded into the service via `EnvironmentFile=` in
`discordbot.service`. Secrets live only in `.env` — never commit it.

## First-time setup (new Pi / fresh install)

```bash
cd ~/MissionBot
git pull
cp .env.sample .env          # then edit .env: set DISCORD_TOKEN + MISSION_CHANNEL_ID
chmod 600 .env
python3 -m pip install -U discord.py
sudo cp discordbot.service /etc/systemd/system/discordbot.service
sudo systemctl daemon-reload
sudo systemctl enable --now discordbot
```

## Redeploy (routine code/data changes)

After pushing to GitHub:

```bash
cd ~/MissionBot
git pull
sudo systemctl restart discordbot
```

If the service unit itself changed, also reinstall it before restarting:

```bash
cd ~/MissionBot
git pull
sudo cp discordbot.service /etc/systemd/system/discordbot.service
sudo systemctl daemon-reload
sudo systemctl restart discordbot
```

## Verify

```bash
systemctl is-active discordbot
systemctl status discordbot --no-pager | head -5
sudo journalctl -u discordbot -n 30 --no-pager
```

A healthy start logs `discord.gateway: Shard ID None has connected to Gateway`
and the restart counter (`systemctl show discordbot -p NRestarts`) stops climbing.

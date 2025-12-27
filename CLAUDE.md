# MissionBot - Claude Code Context

## Deployment

The bot runs on a Raspberry Pi accessible via SSH:

```bash
ssh pi@pi2.local
```

The repository is located at `~/MissionBot` on the Pi.

### Deploying Updates

After pushing changes to GitHub:

```bash
ssh pi@pi2.local "cd MissionBot && git pull"
```

If there are local changes to discard first:

```bash
ssh pi@pi2.local "cd MissionBot && git checkout . && git pull"
```

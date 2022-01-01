# Webb-Tracker-Bot
This is a discord bot that displays current progress of the James Webb Space Telescope. Based on this github: https://github.com/avatsaev/webb-tracker-api
Add it to your server here! https://discord.com/oauth2/authorize?client_id=926742694435360780&permissions=0&scope=bot 

# Installation
Run the following commands:
```batch
git clone https://github.com/Copperbotte/Webb-Tracker-Bot.git
mkdir webb-tracker-api
git clone https://github.com/avatsaev/webb-tracker-api.git ./webb-tracker-api
docker build -t webb-tracker-api .
```

Create a new file called `Token.env` in the current directory.
Get a bot's discord client secret, and set `Token.env`'s contents to be:
`WEBB_BOT_DISCORD_TOKEN=<token>`

Finally, build the images.
```batch
docker-compose up -d
```

# Wildberries API to Telegram bot
Application requests data from Wildberries API (orders and sales), generates excel file and sends them to the telegram user via bot every 30 minutes.

Inside Dockerfile set environment variables for:
**WB_SELLER_TOKEN** - wildberries seller API token.
**TG_TOKEN** - token for your telegram bot.
**TG_CLIENT_ID** - telegram chat id to send data to.

Run command to build docker image:
```
docker build --network=host -t api_to_bot_image .
```
Then run docker image after:
```
docker run api_to_bot_image
```
To remove unused image:
```
docker rmi api_to_bot_image:latest --force
docker image rm --force $(docker image ls -f 'dangling=true' -q)
```
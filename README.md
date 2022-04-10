# Telegram bot (aiogram)
## Simple template use Docker build and docker-compose
## using poetry

### Installation
```sh
mkdir bot && cd $_
git clone https://github.com/akmalovaa/telegrambot-template-docker .
mv env.example .env
nano .env
```

Change .env past your TOKEN from BotFather (save and quit)

```sh
docker-compose up -d
```



### Сhecking the work
```sh
docker ps
tail -f logs/bot.log
```

### Project plans
- Make Gitlab CI/CD
- Add data base
- Add Flask web intefaces

# Telegram bot (aiogram)
## Simple template use Docker build and docker-compose

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
cat logs/bot.log
```

### project plans
- Make Gitlab CI/CD
- Add data base
- Add Flask web intefaces

Telegram бот для запоминания популярных английских слов. 
Тут указано около 3000 наиболее популярных слов английского языка
В переменных окружения надо проставить API токен бота.

`TELEGRAM_API_TOKEN` — API токен бота

Использование с Docker показано ниже. Предварительно заполните ENV переменные, указанные выше, в Dockerfile

```
docker build -t popular_english_words ./
docker run -d --name popular_english_words -p 8080:8080 popular_english_words
```

Чтобы войти в работающий контейнер:

```
docker exec -it popular_english_words bash
```

# * 9 * * * python /app/telegram_bot/sender.py

from crontab import CronTab

with CronTab(user='root') as cron:
    job = cron.new(command='python /app/telegram_bot/sender.py')
    job.hour.on(9)
import psycopg2
from discord_webhook import DiscordWebhook
from datetime import date
"""
This script will return count of daily entries as notification in Discord
"""
# creating the date object of today's date
todays_date = date.today()
# connection
conn = psycopg2.connect(dbname="axie-data", user="axieDataAdmin", password="AxieInsights#1", host="35.225.243.143")
# create cursor
cur = conn.cursor()
# execute sql
cur.execute(f"select COUNT(id) from sales where DATE(timestamp) = '2021-{todays_date.month}-{todays_date.day}'")
# print result
records = cur.fetchone()
cur.close()
# webhook
discord_hook = 'https://discord.com/api/webhooks/908151926296813618/azLGZIhcnHuyg1N5AyDoeRSY03vqmpCuKvGOZMyYhmF7ZwG2UgbjI-llcvvxOJ0_kcmz'
# execute webhook
webhook = DiscordWebhook(url=discord_hook, content=f"Total number of records added on {todays_date}: {records[0]}")
response = webhook.execute()

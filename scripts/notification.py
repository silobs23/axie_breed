import psycopg2
from discord_webhook import DiscordWebhook
"""
This script will return count of daily entries as notification in Discord
"""
# connection
conn = psycopg2.connect(dbname="axie-data", user="axieDataAdmin", password="AxieInsights#1", host="35.225.243.143")
# create cursor
cur = conn.cursor()
# execute sql
cur.execute("select COUNT(id) from sales where timestamp >= NOW() - '1 day'::INTERVAL;")
# print result
records = cur.fetchone()
cur.close()
# webhook
discord_hook = 'https://discord.com/api/webhooks/908151926296813618/azLGZIhcnHuyg1N5AyDoeRSY03vqmpCuKvGOZMyYhmF7ZwG2UgbjI-llcvvxOJ0_kcmz'
# execute webhook
webhook = DiscordWebhook(url=discord_hook, content=f"Total number of records added in the last 24 hours: {records[0]}")
response = webhook.execute()

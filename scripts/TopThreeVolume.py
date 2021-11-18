from discord_webhook import DiscordWebhook
import psycopg2

discord_hook = 'https://discord.com/api/webhooks/910989853657821184/DGWMllNaepRkXZv3HhwtIX22NlQK7SziY47Ff9uJjo2dOdfGXGihfGb_uTkQq3jLp_TQ'
webhook = DiscordWebhook(url=discord_hook,
                                 content=f"Summary of Top 3 Volume and Price by parts\n\n\n\n")
response = webhook.execute()

try:
    # connect to database
    connection = psycopg2.connect(dbname="axie-data", user="axieDataAdmin", password="AxieInsights#1", host="35.225.243.143")
    cursor = connection.cursor()
    postgreSQL_select_Query = "select backd, hornd, mouthd, taild, class, AVG(price) as avgprice, PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY price) AS medianprice, count(backd) as sales FROM sales WHERE sales.timestamp >= '2021-11-15' group by backd, hornd, mouthd, taild, class having avg(price) >= 0.11 order by sales desc limit 3"
    cursor.execute(postgreSQL_select_Query)
    mobile_records = cursor.fetchall()
    for row in mobile_records:
        back = row[0].strip()
        horn = row[1].strip()
        mouth = row[2].strip()
        tail = row[3].strip()
        Axieclass = row[4].strip()
        AveragePrice = row[5]
        MedianPrice = row[6]
        volume = row[7]

        webhook = DiscordWebhook(url=discord_hook,
                                 content=f"back: {back}\n horn: {horn}\n mouth: {mouth}\n tail: {tail}\n Class: {Axieclass}\n AvgPrice: {AveragePrice}\n MedPrice: {MedianPrice}\n Volume: {volume}\n\n\n\n")
        response = webhook.execute()

except (Exception, psycopg2.Error) as error:
    print("Error while fetching data from PostgreSQL", error)

finally:
    # closing database connection.
    if connection:
        cursor.close()
        connection.close()

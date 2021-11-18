from discord_webhook import DiscordWebhook
import psycopg2
import matplotlib.pyplot as plt
# Not parameterized. Change part name in postgreSQL_selec_QUERY and title for other options
try:
    # connect to database
    connection = psycopg2.connect(dbname="axie-data", user="axieDataAdmin", password="AxieInsights#1", host="35.225.243.143")
    cursor = connection.cursor()
    postgreSQL_select_Query = "select PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY price) AS MedianPrice, DATE(timestamp) as dates FROM (select id, backd, hornd, mouthd, taild, class, price, timestamp FROM sales WHERE timestamp >= '2021-11-15' AND backd = 'back-bidens' AND hornd = 'horn-cactus' AND mouthd = 'mouth-zigzag' AND taild = 'tail-hot-butt' AND breedcount = 3 order by timestamp desc) AS criteria group by DATE(timestamp)"

    cursor.execute(postgreSQL_select_Query)
    mobile_records = cursor.fetchall()
    # Define lists
    yAxis = []
    xAxis = []
    for row in mobile_records:
        yAxis.append(row[0])
        xAxis.append(str(row[1]))

except (Exception, psycopg2.Error) as error:
    print("Error while fetching data from PostgreSQL", error)

finally:
    # closing database connection.
    if connection:
        cursor.close()
        connection.close()


plt.plot(xAxis,yAxis, color='red', marker='o')
plt.title('Median Price for Plant [Bidens, Cactus, Zigzag, Hotbutt]')
plt.xlabel('DATE')
plt.ylabel('MEDIAN PRICE')
plt.grid(True)
#plt.show()
fig1 = plt.gcf()
fig1.savefig(r"/Users/keyurkulkarni/Pictures/axie_median.jpg")
# Return figure to descord via webhook
webhook = DiscordWebhook(url='https://discord.com/api/webhooks/910989853657821184/DGWMllNaepRkXZv3HhwtIX22NlQK7SziY47Ff9uJjo2dOdfGXGihfGb_uTkQq3jLp_TQ')

# send two images
with open(r"/Users/keyurkulkarni/Pictures/axie_median.jpg", "rb") as f:
    webhook.add_file(file=f.read(), filename='example.png')

response = webhook.execute()

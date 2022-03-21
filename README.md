# Axie Breed

This project downloads on-chain transaction data from [axie infinity marketplace](https://marketplace.axieinfinity.com) to a Postgres database on Google Cloud. Sample SQL queries will return trending transaction data. Actionable data and charts are published to discord server using webhooks.

createdb.py : Creates database instance and table with schema <br>
fetch&load.py : Fetches data from API, sanitizes and loads into db table <br>
queries folder : Contains sample SQL queries. Results are shared as text and charts on discord

Reach out to @silobs23 for any changes

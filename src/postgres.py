import pandas as pd
import psycopg2
import logging

logging.basicConfig(level=logging.INFO)

def get_postgres_connection(in_user,in_dbname,in_password,in_host):
    """
    Gernerates Postgres Connection
    
    Args:
        in_user: user name used to authenticate
        in_dbname: database name
        in_password: user password for database
        in_host: host port
    
    Returns:
        conn: postgres connection to database
    """
    try:
        # connect to database
        conn = psycopg2.connect(dbname=in_dbname, user=in_user, password=in_password, host=in_host)
    except:
        logging.info("Cannot connect to Postgres Database of {}".format(str(in_dbname)))
        exit()
    
    return conn

def get_data(sql,in_user,in_dbname,in_password,in_host):
    """
    Get data from Postgres Database
    
    Args:
        sql: SQL query to read data from database
        in_user: user name used to authenticate
        in_dbname: database name
        in_password: user password for database
        in_host: host port

    Returns:
        pdf: pandas dataframe with data from postgres database
    """
    conn_pg = get_postgres_connection(in_user,in_dbname,in_password,in_host)
    pdf = pd.read_sql_query(sql, conn_pg)
    conn_pg.close()

    num_rows = pdf.shape[0]
    logging.info("Number of rows read: {}".format(num_rows))

    return pdf
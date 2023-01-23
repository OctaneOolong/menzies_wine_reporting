"""
code taken from:
[Connecting to your DB instance using IAM authentication and the AWS SDK for Python (Boto3) - Amazon Relational Database Service](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.Connecting.Python.html)
"""

import pymysql
import sys
import boto3
import os

ENDPOINT="menzies-wine-stock.c6rsjco4mere.ap-southeast-2.rds.amazonaws.com"
PORT=3306
USER="jstathakis"
REGION="ap-southeast-2b"
DBNAME="menzies-wine-stock"
os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

#gets the credentials from .aws/credentials
session = boto3.Session(profile_name='default')
client = session.client('rds')

token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USER, Region=REGION)

try:
    conn =  pymysql.connect(host=ENDPOINT, 
                            user=USER,
                            passwd=token,
                            port=PORT,
                            database=DBNAME,
                            ssl_ca='global-bundle.pem'
                            )
    # cur = conn.cursor()
    # cur.execute("""SELECT now()""")
    # query_results = cur.fetchall()
    # print(query_results)
except Exception as e:
    print("Database connection failed due to {}".format(e))          
                


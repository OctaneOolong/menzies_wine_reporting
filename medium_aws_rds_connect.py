"""
Code taken from: [Creating an AWS RDS MySQL instance and connect to it using Python. | by Kalpana Sharma | Medium](https://er-kalpanasharma.medium.com/creating-an-aws-rds-mysql-instance-and-connect-to-it-using-python-ea6292df3e1c#:~:text=3%29%20Connect%20through%20Tool%20DBeaver&text=Select%20Community%20Edition%20installer%20as%20per%20your%20need.&text=Add%20your%20RDS%20install%20details,while%20creating%20the%20RDS%20instance.)
"""

# Now we will import that package

import pymysql

#We will use connect() to connect to RDS Instance
#host is the endpoint of your RDS instance
#user is the username you have given while creating the RDS instance
#Password is Master pass word you have given 

ENDPOINT = "menzies-wine-stock.c6rsjco4mere.ap-southeast-2.rds.amazonaws.com"

USERNAME = "jstathakis"

PASSWORD = "[)y3*pKEDj|-8-m>4SVB6&q_YvVl"

db = pymysql.connect(host=ENDPOINT, user = USERNAME, password=PASSWORD)
# you have cursor instance here
cursor = db.cursor()
cursor.execute("select version()")
#now you will get the version of MYSQL you have selected on instance
data = cursor.fetchone()
#Lets's create a DB
sql = '''create database kTestDb'''
cursor.execute(sql)
cursor.connection.commit()
#Create a table 
sql = '''
create table person ( id int not null auto_increment,fname text, lname text, primary key (id) )'''
cursor.execute(sql)
#Check if our table is created or not 
sql = '''show tables'''
cursor.execute(sql)
cursor.fetchall()
#Output of above will be (('person',),)
#Insert some records in the table 
sql = ''' insert into person(fname, lname) values('%s', '%s')''' % ('XXX', 'YYY')
cursor.execute(sql)
db.commit()
#Lets select the data from above added table
sql = '''select * from person'''
cursor.execute(sql)
cursor.fetchall()
#Output of above will be ((1, 'XXX', 'YYY'),)
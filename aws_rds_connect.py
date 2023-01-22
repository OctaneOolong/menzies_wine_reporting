# Now we will import that package
import pymysql
#We will use connect() to connect to RDS Instance
#host is the endpoint of your RDS instance
#user is the username you have given while creating the RDS instance
#Password is Master pass word you have given 
db = pymysql.connect(host="Your RDS endpoint", user = "Username added in RDS instance", password="Master password")
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
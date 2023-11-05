import psycopg2
from indexing import config
conn = psycopg2.connect(database=config.db,
                        host=config.host,
                        user=config.host,
                        password=config.password,
                        port=config.port)
cursor = conn.cursor()
s="testing"
i=10
d=[('test1',1),('8',8),('testing3',9)]
query="INSERT INTO \"SearchEngine_Schema\".\"SearchIndex\" (term,disk_position) VALUES "
for i in range(len(d)-1):
    query+=str(d[i])+","
query+=str(d[-1])
print(query)
# cursor.execute("INSERT INTO \"SearchEngine_Schema\".\"SearchIndex\" (term,disk_position) VALUES %s,%s",d)
# cursor.execute(query)
# cursor.execute("DELETE FROM \"SearchEngine_Schema\".\"SearchIndex\"")
# cursor.execute("SELECT * FROM \"SearchEngine_Schema\".\"SearchIndex\"")
cursor.execute("SELECT disk_position from \"SearchEngine_Schema\".\"SearchIndex\" WHERE term='discov'")

retrieved_data=cursor.fetchall()
print(len(retrieved_data))
for i in retrieved_data:
    print(i[0])
# conn.commit()

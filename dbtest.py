import psycopg2
conn = psycopg2.connect(database="postgres",
                        host="127.0.0.1",
                        user="postgres",
                        password="Jinsakai@25",
                        port="5432")
cursor = conn.cursor()
s="testing"
i=10
d=[('test1',1),('testing1',10),('8',8)]
query=f"INSERT INTO \"SearchEngine_Schema\".\"SearchIndex\" (term,disk_position) VALUES (\'{s}\',{i})"
cursor.execute("INSERT INTO \"SearchEngine_Schema\".\"SearchIndex\" (term,disk_position) VALUES %s,%s",d)
# cursor.execute("DELETE FROM \"SearchEngine_Schema\".\"SearchIndex\"")
cursor.execute("SELECT * FROM \"SearchEngine_Schema\".\"SearchIndex\"")

retrieved_data=cursor.fetchall()
for i in retrieved_data:
    print(i)
conn.commit()

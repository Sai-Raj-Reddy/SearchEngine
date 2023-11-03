import struct
import psycopg2
import math
class DiskIndexWriter():
    def writeIndex(self,index,corpus):
        queries_mapping=[]
        conn = psycopg2.connect(database="postgres",
                        host="127.0.0.1",
                        user="postgres",
                        password="Jinsakai@25",
                        port="5432")
        cursor=conn.cursor()
        l_d_dict={} # To calculate l_d length storing the doc_id as we encounter for each term in the index
        with open('BinaryFiles/disk_postings.bin', 'wb') as file:
            prev_docid=0
            for i in index:
                l=[]
                postings=index[i]
                dft=len(postings) # number of docs the word is appearing
                l.append(dft)
                prev_docid=0
                j=0
                while(j<len(postings)):
                    l.append(postings[j].doc_id-prev_docid) # diff of prev docid with current docid for this term
                    prev_docid=postings[j].doc_id
                    positions=postings[j].positions
                    tftd=len(positions)
                    l.append(tftd) # tftd - number of times the term is appearing in the doc
                    prev_position=0
                    if postings[j].doc_id not in l_d_dict: # if doc_id not already present in l_d dictionary then adding it
                        l_d_dict[postings[j].doc_id]=0
                    l_d_dict[postings[j].doc_id]+=(tftd**2) # square of tftd
                    k=0
                    while(k<tftd):
                        l.append(positions[k]-prev_position) # diff of prev position and current position
                        prev_position=positions[k]
                        k+=1
                    j+=1
                current_position=file.tell()
                # print(l)
                queries_mapping.append((i,current_position))
                packed_data=struct.pack("i"*len(l),*l)
                file.write(packed_data)
        print(queries_mapping)
        query=f"INSERT INTO \"SearchEngine_Schema\".\"SearchIndex\" (term,disk_position) VALUES ('{i}',{current_position})"
        cursor.execute("INSERT INTO \"SearchEngine_Schema\".\"SearchIndex\" (term,disk_position) VALUES %s,%s",queries_mapping)
#             cursor.execute("INSERT INTO \"SearchEngine_Schema\".\"SearchIndex\" (term,disk_position) VALUES %s,%s",d)
# TypeError: not all arguments converted during string formatting
# Maybe integer in term like '8' causing this error check dbtest file for more info or %s,%s is only taking two tuples and giving error for third one
        # print(query)
                # store the term and current_position to database
        conn.commit()
        file.close()
        cursor.close()
        with open('BinaryFiles/docWeights_test1.bin', 'wb') as file:
            for d in corpus:
                try:
                    L_d=math.sqrt(l_d_dict[d.id])
                    packed_data=struct.pack("d",L_d)
                    file.write(packed_data)
                except KeyError as e:
                    print("Exception occurred while writing eucladian length")
                    print("doc_id not present in l_d_dict")
                    print("doc_id ",d.id)
                    print(e)
                except Exception as e:
                    print("Exception occurred while writing eucladian length")
                    print(e)
        file.close()

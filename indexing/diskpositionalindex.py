from typing import Iterable
from .postings import Posting
from .index import Index
import psycopg2
import struct
from text import basictokenprocessor_spanish,basictokenprocessor
from langdetect import detect

class DiskPositionalIndex(Index):
    def __init__(self):
        self.path='BinaryFiles\disk_postings.bin'

        self.conn = psycopg2.connect(database="db",
                        host="host",
                        user="user",
                        password="password",
                        port="port")
        self.cursor=self.conn.cursor()
        # self.p=basictokenprocessor_spanish.BasicTokenProcessorSpanish()
        self.p=basictokenprocessor.BasicTokenProcessor()

    def get_term_position(self,term):
        self.cursor.execute(f"SELECT disk_position from \"SearchEngine_Schema\".\"SearchIndex\" WHERE term='{term}'")
        result=self.cursor.fetchall()
        if len(result)==0:
            return -1
        for i in result:
            return i[0]

    def get_postings(self,term):
        # if detect(term)=='es':
        #     lang='es'
        # else:
        #     lang='en'

        # processed_term=self.p.process_token(term,lang)[0]
        # if term=='Latinoamérica':
        #     print(term,processed_term,lang)
        processed_term=self.p.process_token(term)[0]
        term_position=self.get_term_position(processed_term)
        if term_position==-1:
            return []
        with open(self.path,'rb') as file:
            try:
                file.seek(term_position)
            except Exception as e:
                print("Exception occurred while seeking to the position of term in postings.bin file")
                print(e)
            dft=struct.unpack("i",file.read(4))[0] # checkif it's unpacking dft as expected and then loop for range in dft then cal doc_id from gap and then positions from positions gap
            print("dft",dft)
            postings=[]
            prev_doc_id=0
            for _ in range(dft):
                doc_id_gap=struct.unpack("i",file.read(4))[0] #doc_id gap
                doc_id=prev_doc_id+doc_id_gap
                p=Posting(doc_id)
                with open('BinaryFiles\docWeights.bin','rb') as l_d_file:
                    try:
                        l_d_file.seek(doc_id)
                        l_d=struct.unpack("d",l_d_file.read(8))
                        print(doc_id," ",l_d)
                    except Exception as e:
                        print("Exception occurred while l_d from doc weights file")
                        print(e)
                prev_doc_id=doc_id
                tftd=struct.unpack("i",file.read(4))[0] # number of terms in this doc
                prev_position_id=0
                for m in range(tftd):
                    position_id_gap=struct.unpack("i",file.read(4))[0] #position id gap
                    position=prev_position_id+position_id_gap
                    prev_position_id=position
                    p.add_position(position)
                postings.append(p)
            
        file.close()
        return postings
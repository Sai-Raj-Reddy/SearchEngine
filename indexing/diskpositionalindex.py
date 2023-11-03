from typing import Iterable
from .postings import Posting
from .index import Index
import psycopg2
import struct

class DiskPositionalIndex(Index):
    def __init__(self):
        self.path='BinaryFiles\document_corpus_JSON_stemmed_diskwriter.bin'

        self.conn = psycopg2.connect(database="postgres",
                        host="127.0.0.1",
                        user="postgres",
                        password="Jinsakai@25",
                        port="5432")
        self.cursor=self.conn.cursor()

    def get_term_position(self,term):
        self.cursor.execute("SELECT disk_position from \"SearchEngine_Schema\".\"SearchIndex\" WHERE term='{term}'")
        result=self.cursor.fetchall()
        if len(result)==0:
            return -1
        for i in result:
            return i

    def get_postings(self,term):
        term_position=self.get_term_position(term)
        if term_position==-1:
            return []
        with open(self.path,'rb') as file:
            try:
                file.seek(term_position)
            except Exception as e:
                print("Exception occurred while seeking to the position of term in postings.bin file")
                print(e)
            dft=struct.unpack("i",file.read(4))[0] # checkif it's unpacking dft as expected and then loop for range in dft then cal doc_id from gap and then positions from positions gap
        

        file.close()
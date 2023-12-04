# from typing import Iterable
from .postings import Posting
from .index import Index
import psycopg2
import struct
from text import basictokenprocessor_spanish,basictokenprocessor
# from langdetect import detect
import math
from queue import PriorityQueue

class RankedRetrievalIndex(Index):
    def __init__(self):
        self.path='BinaryFiles\disk_postings.bin'
        self.ad_path='BinaryFiles\docWeights_db.bin'
        self.conn = psycopg2.connect(database="postgres",
                        host="127.0.0.1",
                        user="postgres",
                        password="Jinsakai@25",
                        port="5432")
        self.cursor=self.conn.cursor()
        # self.p=basictokenprocessor_spanish.BasicTokenProcessorSpanish()
        self.p=basictokenprocessor.BasicTokenProcessor()
        self.N=self.get_N()
        # self.a_d_dict={}
        # print(self.N)
        
    def get_N(self):
        self.cursor.execute(f"SELECT COUNT(*) FROM \"SearchEngine_Schema\".\"SearchIndex\"")
        result=self.cursor.fetchall()
        # print(result[0][0])
        return result[0][0]

    def get_term_position(self,term):
        self.cursor.execute(f"SELECT disk_position from \"SearchEngine_Schema\".\"SearchIndex\" WHERE term='{term}'")
        result=self.cursor.fetchall()
        if len(result)==0:
            return -1
        for i in result:
            return i[0]

    def rank_documents(self,query):
        # a_d_values=[]
        dict_a_d={}
        q=PriorityQueue()
        query=query.split(" ")
        for i in query:
            dict_a_d=self.get_postings(i,dict_a_d)
        print(len(dict_a_d))
        with open(self.ad_path,'rb') as l_d_file:
            try:
                for doc_id in dict_a_d:
                    # print(doc_id)
                    # l_d_file.seek(0)
                    l_d_file.seek(doc_id*8)
                    l_d=struct.unpack("d",l_d_file.read(8))[0]
                    a_d=dict_a_d[doc_id]/l_d
                    q.put((a_d*(-1),doc_id))
                # print("doc_id ",doc_id," l_d ",l_d)
            except Exception as e:
                print("Exception occurred while reading l_d from doc weights file")
                print(e)
        l_d_file.close()
        return q
        

    def get_postings(self,term,dict_a_d):
        processed_term=self.p.process_token(term)[0]
        term_position=self.get_term_position(processed_term)
        if term_position==-1:
            return dict_a_d
        with open(self.path,'rb') as file:
            try:
                file.seek(term_position)
            except Exception as e:
                print("Exception occurred while seeking to the position of term in postings.bin file")
                print(e)
            dft=struct.unpack("i",file.read(4))[0] # checkif it's unpacking dft as expected and then loop for range in dft then cal doc_id from gap and then positions from positions gap
            print("dft",dft,"term ",term)
            w_q_t=math.log(1+(self.N/dft))
            postings=[]
            prev_doc_id=0
            for _ in range(dft):
                doc_id_gap=struct.unpack("i",file.read(4))[0] #doc_id gap
                doc_id=prev_doc_id+doc_id_gap
                p=Posting(doc_id)
                # with open('BinaryFiles\docWeights.bin','rb') as l_d_file:
                #     try:
                #         l_d_file.seek(doc_id)
                #         l_d=struct.unpack("d",l_d_file.read(8))
                #         print(doc_id," ",l_d)
                #     except Exception as e:
                #         print("Exception occurred while l_d from doc weights file")
                #         print(e)
                prev_doc_id=doc_id
                tftd=struct.unpack("i",file.read(4))[0] # number of terms in this doc
                # print(tftd)
                if tftd==0:
                    continue
                w_d_t=1+math.log(tftd)
                if doc_id not in dict_a_d:
                    dict_a_d[doc_id]=0
                dict_a_d[doc_id]+=w_d_t*w_q_t
                prev_position_id=0
                for m in range(tftd):
                    position_id_gap=struct.unpack("i",file.read(4))[0] #position id gap
                    position=prev_position_id+position_id_gap
                    prev_position_id=position
                    p.add_position(position)
                postings.append(p)
            
        file.close()
        return dict_a_d
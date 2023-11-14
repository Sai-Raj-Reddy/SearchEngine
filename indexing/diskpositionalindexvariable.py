from typing import Iterable
from .postings import Posting
from .index import Index
import psycopg2
import struct
from text import basictokenprocessor_spanish,basictokenprocessor
from langdetect import detect
# import config


class DiskPositionalIndexVariable(Index):
    def __init__(self):
        self.path='BinaryFiles\disk_postings.bin'

        self.conn = psycopg2.connect(database="postgres",
                        host="127.0.0.1",
                        user="postgres",
                        password="Jinsakai@25",
                        port="5432")
        self.cursor=self.conn.cursor()
        # self.p=basictokenprocessor_spanish.BasicTokenProcessorSpanish()
        self.p=basictokenprocessor.BasicTokenProcessor()

    def get_term_position(self,term):
        self.cursor.execute(f"SELECT disk_position from \"SearchEngine_Schema\".\"SearchIndexVariable\" WHERE term='{term}'")
        result=self.cursor.fetchall()
        if len(result)==0:
            return -1
        for i in result:
            return i[0]

    def decode_encoding(self,bytes_list):
        num=0
        shift=0
        for b in bytes_list:
            data=b&0x7F
            num|=(data<<shift)
            shift+=7
            if not b&0x80:
                break
        return num

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
            data=file.read(1)
            encoded=[]
            if not data[0]&0x80:
                encoded.append(data[0])
            else:
                while data[0]&0x80:
                    encoded.append(data[0])
                    data=file.read(1)
                encoded.append(data[0])
            dft=self.decode_encoding(encoded)
            print("term position ",term_position)
            print("dft ",dft)
            postings=[]
            prev_doc_id=0
            for i in range(dft):
                data=file.read(1)
                encoded=[]
                if not data[0]&0x80:
                    encoded.append(data[0])
                else:
                    while data[0]&0x80:
                        encoded.append(data[0])
                        data=file.read(1)
                    encoded.append(data[0])
                doc_id_gap=self.decode_encoding(encoded)
                doc_id=prev_doc_id+doc_id_gap
                prev_doc_id=doc_id
                p=Posting(doc_id)
                # print("doc_id ",doc_id)
                data=file.read(1)
                encoded=[]
                if not data[0]&0x80:
                    encoded.append(data[0])
                else:
                    while data[0]&0x80:
                        encoded.append(data[0])
                        data=file.read(1)
                    encoded.append(data[0])
                tftd=self.decode_encoding(encoded)
                # print("tftd ",tftd)
                prev_position=0
                for j in range(tftd):
                    data=file.read(1)
                    positions_encoded=[]
                    if not data[0]&0x80:
                        positions_encoded.append(data[0])
                    else:
                        while data[0]&0x80:
                            positions_encoded.append(data[0])
                            data=file.read(1)
                        positions_encoded.append(data[0])
                    position_gap=self.decode_encoding(positions_encoded)
                    position=prev_position+position_gap
                    prev_position=position
                    # print("position ",position)
                    p.add_position(position)
                postings.append(p)
            
        file.close()
        return postings
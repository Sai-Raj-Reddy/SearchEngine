from pathlib import Path
from typing import Iterable
from .document import Document
# import ujson
import json


import pandas as pd
import random
import string

class JsonFileDocument(Document):
    def __init__(self, id, path):
        super().__init__(id)
        self.path=path
        # with open(self.path, 'r', encoding='utf-8') as json_file:
        #     json_data = json.load(json_file)
        # self.title=json_data.get("title", "")
        # self.content=json_data.get("body", "")
        self.title=''

    def title(self) -> str:
        return self.title
        # return "Testing"
    
    def get_content(self):
        # return ["Testing"]
        # s=''
        # for i in range(1000):
        #     s+=''.join(random.choices(string.ascii_uppercase +string.digits, k=(random.randint(3, 9))))
        # return [s]
        with open(self.path, 'r', encoding='utf-8') as json_file:
            # s=''
            # for i in range(1000):
                #     s+=''.join(random.choices(string.ascii_uppercase +string.digits, k=(random.randint(3, 9))))
            # return [s]
            # print("opened")
            json_data = json.load(json_file)
        # return [self.json_data.get("body", "")]
        self.content=json_data.get("body", "")
        self.title=json_data.get("title", "")
        return [self.content]


    

    @staticmethod
    def load_from(abs_path: Path, doc_id: int) -> 'JsonFileDocument':
        # with open(abs_path, 'r', encoding='utf-8') as json_file:
            
        #     json_data = json.load(json_file)

        # title = json_data.get("title", "")
        # content = json_data.get("body", "")
        # url = json_data.get("url", "")

        return JsonFileDocument(doc_id, abs_path)
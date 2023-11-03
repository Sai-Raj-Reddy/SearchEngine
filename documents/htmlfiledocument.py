from pathlib import Path
from typing import Iterable
from .document import Document
# import ujson
from bs4 import BeautifulSoup
import os

import random
import string

class HTMLFileDocument(Document):
    def __init__(self, id, path):
        super().__init__(id)
        self.path=path
        self.title=os.path.basename(self.path)

    def title(self) -> str:
        return self.title
    
    def get_content(self):
        
        with open(self.path, 'r',encoding='utf-8') as html_file:
            html_content=html_file.read()
        # print(html_content)
        html_content.replace('\n','-')
        # print(html_content)
        # print(html_content)
        soup=BeautifulSoup(html_content,"html.parser")
        self.content=soup.get_text(' ',strip=True)
        # print(self.content)
        # self.content.replace('\n','-')
        # print([self.content])
        
        return [self.content]


    

    @staticmethod
    def load_from(abs_path: Path, doc_id: int) -> 'HTMLFileDocument':

        return HTMLFileDocument(doc_id, abs_path)
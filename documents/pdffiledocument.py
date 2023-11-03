from pathlib import Path
from typing import Iterable
from .document import Document
# import ujson
import PyPDF2
import os

import random
import string

class PDFFileDocument(Document):
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
        
        with open(self.path, 'rb') as pdf_file:
            pdf_reader=PyPDF2.PdfReader(self.path)
            text=''
            for page_num in range(len(pdf_reader.pages)):
                page=pdf_reader.pages[page_num]
                text+=page.extract_text()
        self.content=[text]
        self.title=os.path.basename(self.path)
        return self.content
        # return [self.json_data.get("body", "")]
        self.content=json_data.get("body", "")
        self.title=json_data.get("title", "")
        return [self.content]


    

    @staticmethod
    def load_from(abs_path: Path, doc_id: int) -> 'PDFFileDocument':
        # with open(abs_path, 'r', encoding='utf-8') as json_file:
            
        #     json_data = json.load(json_file)

        # title = json_data.get("title", "")
        # content = json_data.get("body", "")
        # url = json_data.get("url", "")

        return PDFFileDocument(doc_id, abs_path)
from pathlib import Path
from typing import Iterable
from .document import Document
# import ujson
import json

class JsonFileDocument(Document):
    def __init__(self, id, path):
        super().__init__(id)
        self.path=path
        with open(self.path, 'r', encoding='utf-8') as json_file:
            self.json_data = json.load(json_file)
        self.title=self.json_data.get("title", "")
        self.content=self.json_data.get("body", "")
        # self.url = url

    def title(self) -> str:
        return self.title
    
    def get_content(self):
        # with open(self.path, 'r', encoding='utf-8') as json_file:
        #     self.json_data = json.load(json_file)
        # return [self.json_data.get("body", "")]
        return [self.content]

    @staticmethod
    def load_from(abs_path: Path, doc_id: int) -> 'JsonFileDocument':
        # with open(abs_path, 'r', encoding='utf-8') as json_file:
            
        #     json_data = json.load(json_file)

        # title = json_data.get("title", "")
        # content = json_data.get("body", "")
        # url = json_data.get("url", "")

        return JsonFileDocument(doc_id, abs_path)
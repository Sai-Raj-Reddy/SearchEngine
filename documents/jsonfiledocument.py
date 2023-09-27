from pathlib import Path
from typing import Iterable
from .document import Document
import json

# class JsonFileDocument(Document):
#     def __init__(self, id : int, path : Path):
#         super().__init__(id)
#         self.path = path
#         # self.json_data=json.load(self.path)
#         with open(self.path, 'r', encoding='utf-8') as json_file:
#             self.json_data = json.load(json_file)


#     @property
#     def title(self) -> str:
#         return self.json_data.get("title", "")

#     # returns TextIOWrapper
#     def get_content(self) -> Iterable[str]:
#         return [self.content]

#     @staticmethod
#     def load_from(abs_path : Path, doc_id : int) -> 'JsonFileDocument' :
#         """A factory method to create a TextFileDocument around the given file path."""

#         return JsonFileDocument(abs_path,doc_id)
    

class JsonFileDocument(Document):
    def __init__(self, id, title, content):
        super().__init__(id)
        self.title = title
        self.content = content
        # self.url = url

    def title(self) -> str:
        return self.title

    # def get_content(self)  -> Iterable[str]:
    #     return [self.content]
    
    def get_content(self):
        return [self.content]

    @staticmethod
    def load_from(abs_path: Path, doc_id: int) -> 'JsonFileDocument':
        with open(abs_path, 'r', encoding='utf-8') as json_file:
            # print('Opened Document')
            json_data = json.load(json_file)

        title = json_data.get("title", "")
        content = json_data.get("body", "")
        # url = json_data.get("url", "")

        return JsonFileDocument(doc_id, title, content)
from typing import Iterable
from .postings import Posting
from .index import Index

class PositionalInvertedIndex(Index):
    def __init__(self):
        # self.vocabulary=set()
        self.PositionalIndex={}
    
    def add_Term(self,terms: list,doc_id:int,position:int):
        for term in terms:
            if term not in self.PositionalIndex:
                self.PositionalIndex[term]=[]
                posting=Posting(doc_id)
                posting.add_position(position)
                self.PositionalIndex[term].append(posting)
            else:
                found=False
                for p in self.PositionalIndex[term]:
                    if p.doc_id==doc_id:
                        p.add_position(position)
                        found=True
                        break
                if not found:
                    p=Posting(doc_id)
                    p.add_position(position)
                    self.PositionalIndex[term].append(p)
                    
            # if term=='explor':
            #     print(self.PositionalIndex[term])
            #     for p in self.PositionalIndex[term]:
            #         print(p.doc_id)
            #         print(p.positions)
    
    def get_postings(self, term: str) -> Iterable[Posting]:
        # print("in get postings")
        # print(term)
        if term in self.PositionalIndex:
            # ans=[]
            # # print(self.PositionalIndex[term])
            # for posting in self.PositionalIndex[term]:
            #     ans.append(Posting(posting.doc_id))
            return self.PositionalIndex[term]
            # return [Posting(doc_id) for doc_id in self.PositionalIndex[term]]
        else:
            return []
    
    # def vocabulary(self) -> list:
    #     return sorted(list(self.vocabulary))
from typing import Iterable
from .postings import Posting
from .index import Index

class PositionalInvertedIndex(Index):
    def __init__(self):
        # self.vocabulary=set()
        self.PositionalIndex={}
    
    # def add_Term(self,terms: list,doc_id:int,position:int):
    #     for term in terms:
    #         if term not in self.PositionalIndex:
    #             self.PositionalIndex[term]=[]
    #             posting=Posting(doc_id)
    #             posting.add_position(position)
    #             self.PositionalIndex[term].append(posting)
    #         else:
    #             found=False
    #             for p in self.PositionalIndex[term]:
    #                 if p.doc_id==doc_id:
    #                     p.add_position(position)
    #                     found=True
    #                     break
    #             if not found:
    #                 p=Posting(doc_id)
    #                 p.add_position(position)
    #                 self.PositionalIndex[term].append(p)

    def add_Term(self,terms: list,doc_id:int,position:int):
        for term in terms:
            if term not in self.PositionalIndex:
                self.PositionalIndex[term]=[]
                posting=Posting(doc_id)
                posting.add_position(position)
                self.PositionalIndex[term].append(posting)
            else:
                if self.PositionalIndex[term][-1].doc_id==doc_id:
                    self.PositionalIndex[term][-1].add_position(position)
                else:
                    p=Posting(doc_id)
                    p.add_position(position)
                    self.PositionalIndex[term].append(p)
                # found=False
                # for p in self.PositionalIndex[term]:
                #     if p.doc_id==doc_id:
                #         p.add_position(position)
                #         found=True
                #         break
                # if not found:
                #     p=Posting(doc_id)
                #     p.add_position(position)
                #     self.PositionalIndex[term].append(p)
    
    def get_postings(self, term: str) -> Iterable[Posting]:
        # print("in get postings")
        # print(term)
        # if term[0]=='-':
        #     term=term[1:]
        if term in self.PositionalIndex:
            return self.PositionalIndex[term]
            # return [Posting(doc_id) for doc_id in self.PositionalIndex[term]]
        else:
            return []
    
    # def vocabulary(self) -> list:
    #     return sorted(list(self.vocabulary))
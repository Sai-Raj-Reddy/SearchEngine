from indexing.postings import Posting
from .querycomponent import QueryComponent

class PhraseLiteral(QueryComponent):
    """
    Represents a phrase literal consisting of one or more terms that must occur in sequence.
    """

    # def __init__(self, terms : list[QueryComponent]):
    def __init__(self, terms : [QueryComponent]):
        self.literals = terms


    # def get_postings(self, index) -> list[Posting]:
    def get_postings(self, index) -> [Posting]:
        # TODO: program this method. Retrieve the postings for the individual literals in the phrase,
		# and positional merge them together.
        distance=1
        ans=self.literals[0].get_postings(index)
        # ans=index.get_postings("photo")
        # return []
        for m in range(1,len(self.literals)):
            postings1=ans
            postings2=self.literals[m].get_postings(index)
            current=[]
            i,j=0,0
            while(i<len(postings1) and j<len(postings2)):
                if postings1[i].doc_id==postings2[j].doc_id:
                    l=self.merge_lists(postings1[i].positions,postings2[j].positions,distance)
                    if len(l)>0:
                        p=Posting(postings1[i].doc_id)
                        for k in l:
                            p.add_position(k)
                        current.append(p)
                    i+=1
                    j+=1
                elif postings1[i].doc_id<postings2[j].doc_id:
                    i+=1
                else:
                    j+=1
            ans=current
            distance+=1
        return ans
        

    def merge_lists(self,l1,l2,dist):
        i,j=0,0
        ans=[]
        # print("in second function")
        # print(l1,l2)
        while(i<len(l1) and j<len(l2)):
            
            if l2[j]-l1[i]==dist:
                ans.append(l1[i])
                i+=1
                j+=1
            elif l2[j]-l1[i]<dist:
                j+=1
            else:
                i+=1
        # print(ans)
        return ans

    def __str__(self) -> str:
        return '"' + " ".join(map(str, self.literals)) + '"'
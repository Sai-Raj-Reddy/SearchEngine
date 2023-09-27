from .querycomponent import QueryComponent
from indexing import Index, Posting

from querying import querycomponent 

class AndQuery(QueryComponent):
    def __init__(self, components : list[QueryComponent]):
        # please don't rename the "components" field.
        self.components = components

    def get_postings(self, index : Index) -> list[Posting]:
        # TODO: program the merge for an AndQuery, by gathering the postings of the composed QueryComponents and
		# intersecting the resulting postings.
        # print(self.components)
        ans=self.components[0].get_postings(index)
        # ans=index.get_postings("photo")
        # return []
        for m in range(1,len(self.components)):
            postings1=ans
            postings2=self.components[m].get_postings(index)
            current=[]
            i,j=0,0
            while(i<len(postings1) and j<len(postings2)):
                if postings1[i].doc_id==postings2[j].doc_id:
                    l=self.merge_lists(postings1[i].positions,postings2[j].positions)
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
        return ans
        # for i in self.components:
        #     print(i," in and query class")
        #     print(type(i))
        # result = []
        
        # return result

    def merge_lists(self,l1,l2):
        i,j=0,0
        ans=[]
        # print("in second function")
        # print(l1,l2)
        while(i<len(l1) and j<len(l2)):
            if l2[j]==l1[i]:
                ans.append(l1[i])
                i+=1
                j+=1
            elif l1[i]<l2[j]:
                ans.append(l1[i])
                i+=1
            else:
                ans.append(l2[j])
                j+=1
        if i<len(l1):
            for k in l1[i:]:
                ans.append(k)
            # ans.append(k for k in l1[i:])
        if j<len(l2):
            for k in l2[j:]:
                ans.append(k)
            # ans.append(k for k in l2[j:])
        # print(ans)
        return ans

    def __str__(self):
        return " AND ".join(map(str, self.components))
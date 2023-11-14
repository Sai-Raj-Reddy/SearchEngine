from collections import Counter
import math
from queue import PriorityQueue
class RankedRetrieval:
    def __init__(self, inverted_index, doc_lengths):
        self.inverted_index = inverted_index
        self.doc_lengths = doc_lengths
        self.N=50
        self.doc_freq=doc_freq
        self.a_d_values={}
        self.q=PriorityQueue()
        self.doc_length_A=doc_length_A

    def calculate_tfidf(self, term, doc_id, term_freq):
        tf = term_freq / self.doc_lengths[doc_id]
        idf = math.log(len(self.doc_lengths) / len(self.inverted_index[term]))
        return tf * idf

    # def rank_documents(self, query):
    #     # scores = Counter()

    #     for term in query:
    #         if term in self.inverted_index:
    #             wq_t=math.log(1+(self.N/self.doc_freq[term]))
    #             for doc_id, term_freq in self.inverted_index[term].items():
    #                 # scores[doc_id] += self.calculate_tfidf(term, doc_id, term_freq)
    #                 wd_t=1+math.log(term_freq)
    #                 if doc_id not in self.a_d_values:
    #                     self.a_d_values[doc_id]=0
    #                 self.a_d_values[doc_id]+=(wq_t*wd_t)
    #     for doc,a_d_value in self.a_d_values.items():
    #         a_d=(a_d_value/self.doc_lengths[doc])
    #         self.q.put((a_d*(-1),doc))
    #     # ranked_results = scores.most_common()
    #     return self.q
    

    # This is for Okapi formula
    def rank_documents(self, query):
        # scores = Counter()

        for term in query:
            if term in self.inverted_index:
                wq_t=max(0.1,math.log((self.N-self.doc_freq[term]+0.5)/(self.doc_freq[term]+0.5)))
                for doc_id, term_freq in self.inverted_index[term].items():
                    wd_t_num=(2.2)*(term_freq)
                    wd_t_denum=(1.2)*(0.25+0.75*(self.doc_lengths[doc_id]/self.doc_length_A)+term_freq)
                    wd_t=wd_t_num/wd_t_denum
                    if doc_id not in self.a_d_values:
                        self.a_d_values[doc_id]=0
                    self.a_d_values[doc_id]+=(wq_t*wd_t)
        for doc,a_d_value in self.a_d_values.items():
            # a_d=(a_d_value/self.doc_lengths[doc])
            self.q.put((a_d_value*(-1),doc))
        # ranked_results = scores.most_common()
        return self.q

inverted_index = {"apple": {1: 3, 2: 2}, "orange": {1: 1, 2: 5}, "red": {1: 8, 2: 5}}
doc_freq={"apple": 5, "orange": 6,"red":13}
doc_lengths = {1: 100, 2: 150}
# print((doc_lengths.items()))
doc_length_A=(350/len(doc_lengths.items()))

ranked_retrieval = RankedRetrieval(inverted_index, doc_lengths)

query = ["apple", "orange","red"]
results = ranked_retrieval.rank_documents(query)
print(results.qsize())
while not results.empty():
    next=results.get()
    print(next[0]*(-1),next[1])
    # print(results.get())

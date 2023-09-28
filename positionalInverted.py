from pathlib import Path
from documents import DocumentCorpus, DirectoryCorpus
from indexing import Index, positionalinvertedindex
from text import BasicTokenProcessor, englishtokenstream
import re
import time
from querying import BooleanQueryParser

"""This basic program builds a term-document matrix over the .txt files in 
the same directory as this file."""

def index_corpus(corpus : DocumentCorpus) -> Index:
    token_processor = BasicTokenProcessor()
    PositionalInvertedIndex=positionalinvertedindex.PositionalInvertedIndex()
    doc_count=1
    test=1
    for d in corpus:
        # print(doc_count,end=" ")
        if doc_count%1000==0:
            print(test)
            test+=1
        # print("Index_docs ",doc_count)
        # print(f"Found document {d.title}")
        # start_time = time.time()
        english_token_stream=englishtokenstream.EnglishTokenStream(d.get_content())
        # print("--- %s seconds for EnglishToken stream  ---" % (time.time() - start_time))
        # print(d.get_content())
        # break
        position=1
        # start_time = time.time()
        for i in english_token_stream:
            # print(i)
            # print(token_processor.process_token(i))
            terms=token_processor.process_token(i)
            PositionalInvertedIndex.add_Term(terms,d.id,position)
            position+=1
        # print("--- %s seconds for process token  ---" % (time.time() - start_time))
        doc_count+=1
        # break
        
    # print("Index_docs ",doc_count)

    return PositionalInvertedIndex

    

if __name__ == "__main__":
    start_time = time.time()
    # JSON_FewDocuments
    # JSON_Testing2
    corpus_path = Path('TestingDocuments\JSON')
    d = DirectoryCorpus.load_json_directory(corpus_path, ".json")
    # corpus_path = Path('TestingDocuments\MobyDick10Chapters')
    # d = DirectoryCorpus.load_text_directory(corpus_path, ".txt")
    print("--- %s seconds for directory load  ---" % (time.time() - start_time))
    # Build the index over this directory.
    start_time = time.time()
    index = index_corpus(d)
    # print(index.get_postings("photo"))
    print("--- %s seconds for index corpus ---" % (time.time() - start_time))
    boolean_query=BooleanQueryParser()
    # query="\"Sand Creek Massacr Nation Histor Site Brochur\""
    # query="\"photo galleri\" + learn requir"
    query="explor"
    start_time = time.time()
    result=boolean_query.parse_query(query.lower())
    result=result.get_postings(index)
    if len(result)==0:
        print("The given text is not found in any documents")
    print(len(result))
    print("--- %s seconds for Search  ---" % (time.time() - start_time))
    # for i in result:
        # print(d.get_document(i.doc_id).title)
        # print(i.positions)
    # while(True):
    #     query=input("Enter the single term word(lower case) to search or 'q!' to quit the application\n")
    #     start_time = time.time()
    #     query=query.split(" ")
    #     if len(query)>1:
    #         print("Please enter a single term(lower case) to search in the documents")
    #     elif query[0]=="q!":
    #         break
    #     else:
    #         result=boolean_query.parse_query(query[0].lower())
    #         for i in result.get_postings(index):
    #             print(d.get_document(i.doc_id))
    #             print(i.positions)
    #     print("--- %s seconds for searching ---" % (time.time() - start_time))
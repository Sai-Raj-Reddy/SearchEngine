from pathlib import Path
from documents import DocumentCorpus, DirectoryCorpus
from indexing import Index, positionalinvertedindex
from text import BasicTokenProcessor, englishtokenstream
import re
import time
from querying import BooleanQueryParser


import pickle



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
        # print(type(d.get_content()))
        # break
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

def serialize_index(index,d):
    serialized_index = pickle.dumps(index)
    serialized_corpus=pickle.dumps(d)
    with open('BinaryFiles/index_JSON_stemmed.bin', 'wb') as file:
        file.write(serialized_index)
    with open('BinaryFiles/document_corpus_JSON_stemmed.bin', 'wb') as file:
        file.write(serialized_corpus)


if __name__ == "__main__":
    # corpus_path = Path('TestingDocuments\JSON_FewDocuments')
    # d = DirectoryCorpus.load_json_directory(corpus_path, ".json")

    try:
        with open('BinaryFiles/index_JSON_stemmed.bin', 'rb') as file:
            serialized_index = file.read()
            index = pickle.loads(serialized_index)
        with open('BinaryFiles/document_corpus_JSON_stemmed.bin', 'rb') as file:
            serialized_index = file.read()
            d = pickle.loads(serialized_index)
        print("loaded from files")
        
    except FileNotFoundError:
        print("File Not Found")
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
        serialize_index(index,d)
        # serialize_index(d)
        # print(index.get_postings("photo"))
        print("--- %s seconds for index corpus ---" % (time.time() - start_time))
    boolean_query=BooleanQueryParser()
    # query="\"Sand Creek Massacr Nation Histor Site Brochur\""
    # query="\"photo galleri\" + learn requir"
    # query="park -science"
    # query="\"Explore this park\" science"
    # query=input("Enter the query ")
    # start_time = time.time()
    # result=boolean_query.parse_query(query.lower())
    # result=result.get_postings(index)
    # for i in result:
    #     # print(d.get_document(i.doc_id).title) # For opening docs in the get_content
    #     print(d.get_document(i.doc_id))
    #     # print(i.doc_id)
    #     print(i.positions)
    #     break
    # if len(result)==0:
    #     print("The given text is not found in any documents")
    # print("No. of documents ",len(result))
    # print("--- %s seconds for Search  ---" % (time.time() - start_time))
    # for i in result:
        # print(d.get_document(i.doc_id).title)
        # print(i.positions)
    while(True):
        query=input("Enter text to search or 'q!' to quit the application\n")
        start_time = time.time()
        # query=query.split(" ")
        if query=="q!":
            break
        else:
            result=boolean_query.parse_query(query)
            result=result.get_postings(index)
            if len(result)==0:
                print("The given text is not found in any documents")
                continue
            for i in result:
                print(d.get_document(i.doc_id))
                print(i.positions)
                # break
            print("No. of documents ",len(result))
        print("--- %s seconds for searching ---" % (time.time() - start_time))
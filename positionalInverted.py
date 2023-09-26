from pathlib import Path
from documents import DocumentCorpus, DirectoryCorpus
from indexing import Index, positionalinvertedindex
from text import BasicTokenProcessor, englishtokenstream
import re
import time

"""This basic program builds a term-document matrix over the .txt files in 
the same directory as this file."""

def index_corpus(corpus : DocumentCorpus) -> Index:
    print("Testing")
    token_processor = BasicTokenProcessor()
    PositionalInvertedIndex=positionalinvertedindex.PositionalInvertedIndex()
    doc_count=1
    for d in corpus:
        # print("Testing")
        print("Index_docs ",doc_count)
        # print(f"Found document {d.title}")
        english_token_stream=englishtokenstream.EnglishTokenStream(d.get_content())
        # print(d.get_content())
        # break
        position=1
        for i in english_token_stream:
            # print(i)
            # print(token_processor.process_token(i))
            terms=token_processor.process_token(i)
            PositionalInvertedIndex.add_Term(terms,d.id,position)
            position+=1
        doc_count+=1
    print("Index_docs ",doc_count)

    return PositionalInvertedIndex

    

if __name__ == "__main__":
    start_time = time.time()
    corpus_path = Path('TestingDocuments\JSON_Testing2')
    d = DirectoryCorpus.load_json_directory(corpus_path, ".json")
    # corpus_path = Path('TestingDocuments\MobyDick10Chapters')
    # d = DirectoryCorpus.load_text_directory(corpus_path, ".txt")
    print("--- %s seconds for directory load  ---" % (time.time() - start_time))
    # Build the index over this directory.
    start_time = time.time()
    print("Testing")
    index = index_corpus(d)
    print("--- %s seconds for index corpus ---" % (time.time() - start_time))
    while(True):
        query=input("Enter the single term word(lower case) to search or 'q!' to quit the application\n")
        start_time = time.time()
        query=query.split(" ")
        if len(query)>1:
            print("Please enter a single term(lower case) to search in the documents")
        elif query[0]=="q!":
            break
        else:
            result=index.get_postings(query[0].lower())
            if len(result)==0:
                print("The given term is not found in any documents")
            else:
                # print(result)
                for p in result:
                    print(f"Found in {d.get_document(p.doc_id)}")
                    print(p.positions)
        print("--- %s seconds for searching ---" % (time.time() - start_time))
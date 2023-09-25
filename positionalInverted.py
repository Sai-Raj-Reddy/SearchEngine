from pathlib import Path
from documents import DocumentCorpus, DirectoryCorpus
from indexing import Index, positionalinvertedindex
from text import BasicTokenProcessor, englishtokenstream
import re

"""This basic program builds a term-document matrix over the .txt files in 
the same directory as this file."""

def index_corpus(corpus : DocumentCorpus) -> Index:
    
    token_processor = BasicTokenProcessor()
    PositionalInvertedIndex=positionalinvertedindex.PositionalInvertedIndex()
    for d in corpus:
        print(f"Found document {d.title}")
        english_token_stream=englishtokenstream.EnglishTokenStream(d.get_content())
        position=1
        for i in english_token_stream:
            # print(token_processor.process_token(i))
            terms=token_processor.process_token(i)
            PositionalInvertedIndex.add_Term(terms,d.id,position)
            position+=1

    return PositionalInvertedIndex

    

if __name__ == "__main__":
    corpus_path = Path('TestingDocuments\MobyDick10Chapters')
    d = DirectoryCorpus.load_text_directory(corpus_path, ".txt")

    # Build the index over this directory.
    index = index_corpus(d)
    
    while(True):
        query=input("Enter the single term word(lower case) to search or 'q!' to quit the application\n")
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
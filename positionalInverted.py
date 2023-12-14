from pathlib import Path
from documents import DocumentCorpus, DirectoryCorpus
from indexing import Index, positionalinvertedindex,diskindexwriter,diskpositionalindex,diskpositionalindexvariable,diskindexwritervariable,rankedretrievalindex
from text import BasicTokenProcessor, englishtokenstream,spanishtokenstream,basictokenprocessor_spanish
# spanishtokenstream
import re
import time
from querying import BooleanQueryParser


from langdetect import detect

import pickle
import struct





def index_corpus(corpus : DocumentCorpus) -> Index:
    token_processor = BasicTokenProcessor()
    # token_processor=basictokenprocessor_spanish.BasicTokenProcessorSpanish()
    PositionalInvertedIndex=positionalinvertedindex.PositionalInvertedIndex()
    doc_count=1
    test=1
    for d in corpus:
        # print(doc_count,end=" ")
        if doc_count%1000==0:
            print(test)
            test+=1
        # print(d.id)
        # print("Index_docs ",doc_count)
        # print(f"Found document {d.title}")
        # start_time = time.time()
        # print(type(d.get_content()))
        # break


        # token_stream=englishtokenstream.EnglishTokenStream(d.get_content())
        position=1


        # This is for langdetect
        # text=d.get_content()[0]
        # if d.id==13:
        #     print(text)
        # if detect(text)=='es':
        #     lang='es'
        #     # token_stream=spanishtokenstream.SpanishTokenStream(text)
        #     # token_stream=englishtokenstream.EnglishTokenStream(d.get_content())
        # else:
        #     lang='en'
        #     # token_stream=englishtokenstream.EnglishTokenStream(d.get_content())


        token_stream=englishtokenstream.EnglishTokenStream(d.get_content())
        # when commenting this also comment import and change token_processor back to basictokenprocessor and change process token function call in below loop


        for i in token_stream:
            # print(i)
            # if d.id==13:
            #     print(i)
            # if lang=='es':
            #     print(i)
            # print(i)
            terms=token_processor.process_token(i)
            # terms=token_processor.process_token(i,lang)
            # if d.id==13:
            #     print(i,terms)
            # if lang=='es':
            #     print(terms)
            # print(terms)
            PositionalInvertedIndex.add_Term(terms,d.id,position)
            position+=1
        # print("--- %s seconds for process token  ---" % (time.time() - start_time))
        doc_count+=1
        # break
        
    # print("Index_docs ",doc_count)

    return PositionalInvertedIndex


# def index_corpus_doc_length(corpus : DocumentCorpus) -> Index:
#     token_processor = BasicTokenProcessor()
#     PositionalInvertedIndex=positionalinvertedindex.PositionalInvertedIndex()
#     doc_count=0
#     test=1
#     total_length=0
#     with open('BinaryFiles/doclengths.bin', 'wb') as file:
#         for d in corpus:
#             if doc_count%1000==0:
#                 print(test)
#                 test+=1
#             doc_length=0
#             token_stream=englishtokenstream.EnglishTokenStream(d.get_content())
#             for i in token_stream:
#                 terms=token_processor.process_token(i)
#                 doc_length+=len(terms)
#             total_length+=doc_length
#             doc_count+=1
#             packed_data=struct.pack("i",doc_length)
#             file.write(packed_data)
#         print("total length ",total_length)
#         print("doc_count ",doc_count)

#     return PositionalInvertedIndex

def serialize_index(index,d):
    # serialized_index = pickle.dumps(index)
    # serialized_corpus=pickle.dumps(d)
    # with open('BinaryFiles/index_JSON_Positional_Index.bin', 'wb') as file:
    #     file.write(serialized_index)
    # with open('BinaryFiles/document_corpus_JSON_Positional_Index.bin', 'wb') as file:
    #     file.write(serialized_corpus)
    serialized_index = pickle.dumps(index)
    serialized_corpus=pickle.dumps(d)
    with open('BinaryFiles/index_JSON_Positional_Index_Final.bin', 'wb') as file:
        file.write(serialized_index)
    with open('BinaryFiles/document_corpus_JSON_Positional_Index_Final.bin', 'wb') as file:
        file.write(serialized_corpus)


# if __name__ == "__main__":
#     # corpus_path = Path('TestingDocuments\JSON_FewDocuments')
#     # d = DirectoryCorpus.load_json_directory(corpus_path, ".json")
#     # corpus_path = Path('TestingDocuments\PDF')
#     # d = DirectoryCorpus.load_pdf_directory(corpus_path,".pdf")

#     # corpus_path = Path('TestingDocuments\HTMLFiles')
#     # d = DirectoryCorpus.load_html_directory(corpus_path,".html")
#     # index = index_corpus(d)

#     try:
#         # with open('BinaryFiles/index_JSON_Positional_Index.bin', 'rb') as file:
#         #     serialized_index = file.read()
#         #     index = pickle.loads(serialized_index)
#         # with open('BinaryFiles/document_corpus_JSON_Positional_Index.bin', 'rb') as file:
#         #     serialized_index = file.read()
#         #     d = pickle.loads(serialized_index)
#         # print("loaded from files")
#         with open('BinaryFiles/index_JSON_Positional_Index_Final.bin', 'rb') as file:
#             serialized_index = file.read()
#             index = pickle.loads(serialized_index)
#         with open('BinaryFiles/document_corpus_JSON_Positional_Index_Final.bin', 'rb') as file:
#             serialized_index = file.read()
#             d = pickle.loads(serialized_index)
#         print("loaded from files")
        
#     except FileNotFoundError:
#         print("File Not Found")
#         start_time = time.time()
#         # JSON_FewDocuments
#         # JSON_Testing2
#         corpus_path = Path('TestingDocuments\JSON')
#         d = DirectoryCorpus.load_json_directory(corpus_path, ".json")
#         # corpus_path = Path('TestingDocuments\MobyDick10Chapters')
#         # d = DirectoryCorpus.load_text_directory(corpus_path, ".txt")
#         print("--- %s seconds for directory load  ---" % (time.time() - start_time))
#         # Build the index over this directory.
#         start_time = time.time()
#         index = index_corpus(d)
#         serialize_index(index,d)
#         # serialize_index(d)
#         # print(index.get_postings("photo"))
#         print("--- %s seconds for index corpus ---" % (time.time() - start_time))
#     start_time = time.time()
#     diskwriter=diskindexwriter.DiskIndexWriter()
#     diskwriter.writeIndex(index.get_index(),d)
#     # diskwriter=diskindexwritervariable.DiskIndexWriterVariable()
#     # diskwriter.writeIndex(index.get_index(),d)
#     print("--- %s seconds for disk and database writing  ---" % (time.time() - start_time))
#     # index=diskpositionalindex.DiskPositionalIndex()
#     # index=diskpositionalindexvariable.DiskPositionalIndexVariable()
#     boolean_query=BooleanQueryParser()
#     # query="\"Sand Creek Massacr Nation Histor Site Brochur\""
#     # query="\"photo galleri\" + learn requir"
#     # query="park -science"
#     # query="\"Explore this park\" science"
#     # query=input("Enter the query ")
#     # start_time = time.time()
#     # result=boolean_query.parse_query(query.lower())
#     # result=result.get_postings(index)
#     # for i in result:
#     #     # print(d.get_document(i.doc_id).title) # For opening docs in the get_content
#     #     print(d.get_document(i.doc_id))
#     #     # print(i.doc_id)
#     #     print(i.positions)
#     #     break
#     # if len(result)==0:
#     #     print("The given text is not found in any documents")
#     # print("No. of documents ",len(result))
#     # print("--- %s seconds for Search  ---" % (time.time() - start_time))
#     # for i in result:
#         # print(d.get_document(i.doc_id).title)
#         # print(i.positions)
#     while(True):
#         query=input("Enter text to search or 'q!' to quit the application\n")
#         start_time = time.time()
#         # query=query.split(" ")
#         if query=="q!":
#             break
#         else:
#             result=boolean_query.parse_query(query)
#             result=result.get_postings(index)
#             if len(result)==0:
#                 print("The given text is not found in any documents")
#                 continue
#             for i in result:
#                 print(d.get_document(i.doc_id))
#                 print(i.positions)
#                 # break
#             print("No. of documents ",len(result))
#         print("--- %s seconds for searching ---" % (time.time() - start_time))


# # This is for calculating doc_lengths
# if __name__ == "__main__":
#     try:
#         with open('BinaryFiles/not_imp/index_JSON_Positional_Index_doc_length.bin', 'rb') as file:
#             serialized_index = file.read()
#             index = pickle.loads(serialized_index)
#         with open('BinaryFiles/not_imp/document_corpus_JSON_Positional_Index_doc_length.bin', 'rb') as file:
#             serialized_index = file.read()
#             d = pickle.loads(serialized_index)
#         print("loaded from files")
#     except FileNotFoundError:
#         print("File Not Found")
#         start_time = time.time()
#         corpus_path = Path('TestingDocuments\JSON')
#         d = DirectoryCorpus.load_json_directory(corpus_path, ".json")
#         print("--- %s seconds for directory load  ---" % (time.time() - start_time))
#         start_time = time.time()
#         index = index_corpus_doc_length(d)
#         print("--- %s seconds for index corpus ---" % (time.time() - start_time))

# # This is for database search -working diskpositional index
# if __name__ == "__main__":
#     # index=diskpositionalindex.DiskPositionalIndex()
#     # index=diskpositionalindexvariable.DiskPositionalIndexVariable()
#     index=diskpositionalindex.DiskPositionalIndex()
#     # index.get_postings('discover')
#     boolean_query=BooleanQueryParser()
#     with open('BinaryFiles\document_corpus_JSON_Positional_Index.bin', 'rb') as file:
#         serialized_index = file.read()
#         d = pickle.loads(serialized_index)
#     while(True):
#         query=input("Enter text to search or 'q!' to quit the application\n")
#         start_time = time.time()
#         # query=query.split(" ")
#         if query=="q!":
#             break
#         else:
#             result=boolean_query.parse_query(query)
#             result=result.get_postings(index)
#             if len(result)==0:
#                 print("The given text is not found in any documents")
#                 continue
#             for i in result:
#                 print(d.get_document(i.doc_id))
#                 print(i.positions)
#                 # break
#             print("No. of documents ",len(result))
#         print("--- %s seconds for searching ---" % (time.time() - start_time))

# This is for ranked retrieval- wrong - use diskpositionalindex since it has tf-idf
if __name__ == "__main__":
    # index=diskpositionalindex.DiskPositionalIndex()
    # index=diskpositionalindexvariable.DiskPositionalIndexVariable()
    index=rankedretrievalindex.RankedRetrievalIndex()
    # index.get_postings('discover')
    boolean_query=BooleanQueryParser()
    with open('BinaryFiles\document_corpus_JSON_Positional_Index.bin', 'rb') as file:
        serialized_index = file.read()
        d = pickle.loads(serialized_index)
    while(True):
        query=input("Enter text to search or 'q!' to quit the application\n")
        start_time = time.time()
        # query=query.split(" ")
        if query=="q!":
            break
        else:
            # result=boolean_query.parse_query(query)
            # result=index.rank_documents(query)
            result=index.rank_okapi(query)
            # result=result.get_postings(index)
            if result.qsize()==0:
                print("The given text is not found in any documents")
                continue
            if result.qsize()<10:
                while not result.empty():
                    next=result.get()
                    print(d.get_document(next[1]),next[0]*(-1))
            else:
                for i in range(10):
                    next=result.get()
                    print(d.get_document(next[1]),next[0]*(-1))
                # break
            # print("No. of documents ",result.qsize())
        print("--- %s seconds for searching ---" % (time.time() - start_time))
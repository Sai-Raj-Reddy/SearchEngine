import PyPDF2
from text import BasicTokenProcessor, englishtokenstream
pdf_path='TestingDocuments\PDF\Assignment2.pdf'
with open(pdf_path,'rb') as pdf_file:
    pdf_reader=PyPDF2.PdfReader(pdf_path)
    text=''
    token_processor = BasicTokenProcessor()
    for page_num in range(len(pdf_reader.pages)):
        page=pdf_reader.pages[page_num]
        # page=pdf_reader.getPage(page_num)
        text+=page.extract_text()
        
        # print(text[0])
        # break
    # file1=open('Testing_assignment_nostem.txt','w')
    # file2=open('Testing_assignment_stem.txt','w')
    # file1.write(text)
    
    text=[text]
    english_token_stream=englishtokenstream.EnglishTokenStream(text)
    position=1
    # start_time = time.time()
    for i in english_token_stream:
        # print(i,position)
        # file1.write(i)
        # file1.write('\t')
        # file1.write(str(position))
        # file1.write('\n')
        # print(token_processor.process_token(i))
        terms=token_processor.process_token(i)
        # for j in terms:
        #     file2.write(j)
        #     file2.write('\t')
        #     file2.write(str(position))
        #     file2.write('\n')
        # print(terms)
        # PositionalInvertedIndex.add_Term(terms,d.id,position)
        position+=1
        # if position==10:
        #     break
    # file1.close()
    # file2.close()
import sys
import struct


def encode_number(number):
    bytes_list=[]
    while True:
        byte=number&0x7F
        number>>=7
        if number==0:
            byte&=0x7F
        else:
            byte|=0x80
        bytes_list.append(byte)
        if number==0:
            break
    return bytes_list

def decode_encoding(bytes_list):
    num=0
    shift=0
    for b in bytes_list:
        data=b&0x7F
        num|=(data<<shift)
        shift+=7
        if not b&0x80:
            break
    return num



# integer_my=128
# integers_list_nums=[128,127]
integers_list=[3,2,2,0,2,3,1,5,4,5,0,7,9,10,560]
# for i in range(1000):
#     integers_list.append(integers_list_nums[0])
#     integers_list.append(integers_list_nums[1])
print(encode_number(128))
# print(bin(128))
# # print(sys.getsizeof(integer_my))
# bits_rep=bin(128)[2:]
# print(bits_rep)
# binary=integer_my&0x7F
# print(binary)
# integer_my>>=7
# print(integer_my)
# # print(integer_my&0x7F)
# with open("encoded_data.bin","wb") as file:
#     packed_data=struct.pack("i"*len(integers_list),*integers_list)
#     file.write(packed_data)

with open("variable_encoded_data_testing.bin","wb") as file:
    for i in integers_list:
        encoded_bytes=encode_number(i)
        file.write(bytes(encoded_bytes))
        print(file.tell())

# with open("variable_encoded_data_testing.bin","rb") as file:
#     i=1
#     while True:
#         encoded=[]
#         data=file.read(1)
        
#         if not data:
#             break
#         if not data[0]&0x80:
#             encoded.append(data[0])
#         else:
#             while data[0]&0x80:
#                 encoded.append(data[0])
#                 data=file.read(1)
#                 i+=1
#             encoded.append(data[0])
#         num=decode_encoding(encoded)
#             # break
#         # print(data[0]&0x80)
#         print(num)
#         if i==10:
#             break
        
#         # break

with open("variable_encoded_data_testing.bin","rb") as file:
    file.seek(15)
    data=file.read(1)
    encoded=[]
    if not data[0]&0x80:
        encoded.append(data[0])
    else:
        while data[0]&0x80:
            encoded.append(data[0])
            data=file.read(1)
        encoded.append(data[0])
    num=decode_encoding(encoded)
    print("dft ",num)
    # postings_list=[]
    # prev_doc_id=0
    # for i in range(num):
    #     data=file.read(1)
    #     encoded=[]
    #     if not data[0]&0x80:
    #         encoded.append(data[0])
    #     else:
    #         while data[0]&0x80:
    #             encoded.append(data[0])
    #             data=file.read(1)
    #         encoded.append(data[0])
    #     doc_id_gap=decode_encoding(encoded)
    #     doc_id=prev_doc_id+doc_id_gap
    #     prev_doc_id=doc_id
    #     # p=Posting(doc_id)
    #     print("doc_id ",doc_id)
    #     data=file.read(1)
    #     encoded=[]
    #     if not data[0]&0x80:
    #         encoded.append(data[0])
    #     else:
    #         while data[0]&0x80:
    #             encoded.append(data[0])
    #             data=file.read(1)
    #         encoded.append(data[0])
    #     tftd=decode_encoding(encoded)
    #     print("tftd ",tftd)
    #     prev_position=0
    #     for j in range(tftd):
    #         data=file.read(1)
    #         positions_encoded=[]
    #         if not data[0]&0x80:
    #             positions_encoded.append(data[0])
    #         else:
    #             while data[0]&0x80:
    #                 positions_encoded.append(data[0])
    #                 data=file.read(1)
    #             positions_encoded.append(data[0])
    #         position_gap=decode_encoding(positions_encoded)
    #         position=prev_position+position_gap
    #         prev_position=position
    #         print("position ",position)
            # p.add_position(position)
        # postings_list.append(p)
file.close()

    
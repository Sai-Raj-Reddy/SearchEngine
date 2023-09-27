from porter2stemmer import Porter2Stemmer

Stemmer=Porter2Stemmer()
l=['requiring']
for i in l:
    print(i,Stemmer.stem(i))

# length_out = 0
# start_index=0
# query="Shakes + Smoothies"
# # Find the start of the next subquery by skipping spaces and + signs.
# test = query[start_index]
# while test == ' ' or test == '+':
#     start_index += 1
#     test = query[start_index]
# print(test)
# # Find the end of the next subquery.
# next_plus = query.find("+", start_index + 1)
# print(next_plus)
# if next_plus < 0:
#     # If there is no other + sign, then this is the final subquery in the
# 	# query string.
#     length_out = len(query) - start_index
#     print("length_out",length_out)
# else:
#     # If there is another + sign, then the length of this subquery goes up
# 	# to the next + sign.

# 	# Move next_plus backwards until finding a non-space non-plus character.
#     test = query[next_plus]
#     while test == ' ' or test == '+':
#         next_plus -= 1
#         test = query[next_plus]
#     length_out = 1 + next_plus - start_index
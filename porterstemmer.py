# from porter2stemmer import Porter2Stemmer

# Stemmer=Porter2Stemmer()
# l=['requiring']
# for i in l:
#     print(i,Stemmer.stem(i))

# Create a translation table to remove double quotes
translation_table = str.maketrans('', '', '"\'')

# Input string with double quotes
original_string = '"Hello, "wo\'rld"!"'

# Use the translate method to remove double quotes
unquoted_string = original_string.translate(translation_table)

print(unquoted_string)  # Output: Hello, world!
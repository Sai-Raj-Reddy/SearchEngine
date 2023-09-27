from .tokenprocessor import TokenProcessor
import re
from porter2stemmer import Porter2Stemmer


class BasicTokenProcessor(TokenProcessor):
    """A BasicTokenProcessor creates terms from tokens by removing all non-alphanumeric characters 
    from the token, and converting it to all lowercase."""
    whitespace_re = re.compile(r"\W+")
    Stemmer=Porter2Stemmer()
    def process_token(self, token : str):
        # token=re.sub(self.whitespace_re, "", token)
        # print(token)
        if '-' in token:
            split_tokens=[]
            
            # split_tokens=re.split(r'-',token) # Splitting the tokens removing hyphen
            # split_tokens.append(re.sub(r'-','',token)) # Appending the whole string after removing hyphen
            # print(str(''.join(token.split('-'))))
            complete_str=""
            for i in token.split('-'):
                complete_str+=i
                split_tokens.append(i)
            # str(''.join(token.split('-')))
            split_tokens.append(complete_str)
            # split_tokens.append(str(i) for i in token.split('-'))
            
        else:
            split_tokens=[token]
        # split_tokens=[re.sub(r'^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$','',s) for s in split_tokens if s!=''] # removing non alpha numeric from  beginning and ending and s!='' to remove empty strings for double hyphen words
        non_alphanumeric=[]
        # flag=False
        # print(split_tokens)
        for s in split_tokens:
            if s!='':
                i=0
                j=len(s)-1
                while(i<j):
                    ascii_val=ord(s[i])
                    if (ascii_val>=48 and ascii_val<=57) or (ascii_val>=65 and ascii_val<=90) or (ascii_val>=97 and ascii_val<=122):
                        break
                    else:
                        i+=1
                while(j>=0):
                    ascii_val=ord(s[j])
                    if (ascii_val>=48 and ascii_val<=57) or (ascii_val>=65 and ascii_val<=90) or (ascii_val>=97 and ascii_val<=122):
                        break
                    else:
                        j-=1
                if not i>=len(s) and not j<0:
                    non_alphanumeric.append(s[i:j+1].lower())
        for s in non_alphanumeric:
            s.replace("\'","")
            s.replace("\"","")
        # split_tokens_final=[re.sub(r'\'|"','',s.lower()) for s in split_tokens]
        return non_alphanumeric
        # return [self.normalize(token) for token in non_alphanumeric]
    
    def normalize(self,token: str):
        # return self.Stemmer.ste
        return self.Stemmer.stem(token)
        
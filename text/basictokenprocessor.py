from .tokenprocessor import TokenProcessor
import re
from porter2stemmer import Porter2Stemmer


class BasicTokenProcessor(TokenProcessor):
    """A BasicTokenProcessor creates terms from tokens by removing all non-alphanumeric characters 
    from the token, and converting it to all lowercase."""
    whitespace_re = re.compile(r"\W+")
    Stemmer=Porter2Stemmer()
    def process_token(self, token : str):
        # return [token]
        # # token=re.sub(self.whitespace_re, "", token)
        # split_tokens=[token]
        if '-' in token:
            split_tokens=[]
            complete_str=""
            for i in token.split('-'):
                complete_str+=i
                split_tokens.append(i)
            # str(''.join(token.split('-')))
            split_tokens.append(complete_str)
            # split_tokens.append(str(i) for i in token.split('-'))
            
        else:
            split_tokens=[token]
        
        non_alphanumeric=[]
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
                st=''
                for k in range(i,j+1):
                    if s[k]=='\'' or s[k]=='"':
                        continue
                    else:
                        st+=s[k]
                non_alphanumeric.append(st.lower())
                # non_alphanumeric.append(s[i:j+1])
                # if not i>=len(s) and not j<0:
                #     non_alphanumeric.append(s[i:j+1].lower())
        
        # final_tokens=[]
        # for i in non_alphanumeric:
        #     s=''
        #     for j in i:
        #         if j=='\'' or j=='"':
        #             continue
        #         else:
        #             s+=j
        #     final_tokens.append(s)
        # print([self.normalize(token) for token in non_alphanumeric])
        # return non_alphanumeric
        return [self.normalize(token) for token in non_alphanumeric]
    
    def normalize(self,token: str):
        # return self.Stemmer.ste
        return self.Stemmer.stem(token)
        
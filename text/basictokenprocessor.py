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
            split_tokens=re.split(r'-',token) # Splitting the tokens removing hyphen
            split_tokens.append(re.sub(r'-','',token)) # Appending the whole string after removing hyphen
        else:
            split_tokens=[token]
        split_tokens=[re.sub(r'^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$','',s) for s in split_tokens if s!=''] # removing non alpha numeric from  beginning and ending and s!='' to remove empty strings for double hyphen words
        split_tokens_final=[re.sub(r'\'|"','',s.lower()) for s in split_tokens]
        return [self.normalize(token) for token in split_tokens_final]
    
    def normalize(self,token: str):
        # return self.Stemmer.ste
        return self.Stemmer.stem(token)
        
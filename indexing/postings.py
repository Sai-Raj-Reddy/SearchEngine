class Posting:
    """A Posting encapulates a document ID associated with a search query component."""
    def __init__(self, doc_id : int):
        self.doc_id = doc_id
        self.positions=[]
    
    def add_position(self,position):
        self.positions.append(position)

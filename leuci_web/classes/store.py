

"""
 Straightforward implementation of the Singleton Pattern
 https://python-patterns.guide/gang-of-four/singleton/
 """

class Store(object):
    _instance = None


    def __new__(cls):
        if cls._instance is None:            
            cls._instance = super(Store, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance
    
    def __init__(self):
        self.storage = {}

    def add_or_get(self,pdb_code):
        if pdb_code in self.storage:
            return self.storage[pdb_code]
        else:
            pass
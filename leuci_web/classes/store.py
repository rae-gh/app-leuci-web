
"""
Thread safe implementation of the Singleton Pattern
https://medium.com/analytics-vidhya/how-to-create-a-thread-safe-singleton-class-in-python-822e1170a7f6
See also: https://python-patterns.guide/gang-of-four/singleton/
 """

import threading
import datetime

class Store:
    _instance = None
    _lock = threading.Lock()
    strge = {}
    strge_dates = {}
    
    def __new__(cls):
        if not cls._instance:  # This is the only difference
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance
                        
    def exists(cls,pdb_code):
        return pdb_code in cls.strge
    
    def get(cls,pdb_code):
        dt = cls.strge_dates[pdb_code]
        return cls.strge[pdb_code],dt
    
    def add(cls,pdb_code, map_obj):        
        cls.strge[pdb_code] = map_obj
        cls.strge_dates[pdb_code] = datetime.datetime.now()
            
    def clear(cls):
        cls.strge.clear()
        cls.strge_dates.clear()
                    
    def storage(cls):
        return cls.strge
    
    def storage_dates(cls):
        return cls.strge_dates
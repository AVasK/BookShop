## To be implemented

Year = 2019

class ModelTime: # time in days
    _time = 0
    THRESHOLD = 30 # num. of days a book is concidered NEW.
    # ^ can be set by classmethod .setThreshold(new_threshold)
    
    def __init__(self, n_days_ago = 0):
        self.creation_time = self._time - n_days_ago
        
        
    @classmethod
    def timer(cls, days):
        t0 = cls()
        def timer():
            nonlocal t0
            if t0.time() >= days:
                return True
            return False
        return timer
        
    @classmethod
    def timeStep(cls, days = 1):
        cls._time += days
        
    @classmethod
    def total_time(cls):
        return cls._time
        
    def time(self):
        return self._time - self.creation_time
    
    def is_recent(self):
        return self.time() <= self.THRESHOLD
    
    @classmethod
    def set_threshold(cls, new_threshold):
        cls.THRESHOLD = new_threshold
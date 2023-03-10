import numpy as np


class Experience():

    def __init__(self, path: str):
        self.path = path
        self.name = os.path.basename(self.path)
        return None
    
    def __read_data(self):
        self.data = 
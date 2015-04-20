import numpy as np

#class for importing the file from csv file as an array    
class ImportFile(object):

    def __init__(self):
        pass
        
    def open_file(self, filename):
        entry_data = np.genfromtxt(filename, dtype=None, delimiter=',', skip_header=1, 
        			usecols=(0, 2, 1, 6, 1, 3, 1, 4, 1, 5), invalid_raise=False)
        return entry_data

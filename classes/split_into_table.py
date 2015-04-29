#class with methods that find places where cellnumber changes and divides original array into new, smaller arrays        
class SplitIntoNewTables(object):
    
    def __init__(self):
        pass

    def where_to_split(self, entry_data):
        
        col_3 = entry_data['f1']
        
        change_number = [0]
        counter = 0
        for name_1, name_2 in zip(col_3, col_3[1:]): #find places where cell change (new normalization)
            if name_1.split(':', 1)[1] == name_2.split(':', 1)[1]:
                counter += 1
            else:
                change_number.append(counter+1)
                counter += 1                
        change_number.append(len(entry_data))
        
        return change_number
       
    def make_new_table(self, change_number, entry_data):
        for number_1, number_2 in zip(change_number, change_number[1:]):                
            ready_to_analize_array = entry_data[number_1:number_2]        
            return ready_to_analize_array

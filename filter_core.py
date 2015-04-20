#Start import
import numpy as np
import scipy as sp
from scipy import stats
import os
import matplotlib.pyplot as plt
import collections
from peewee import *
from classes.open_file import ImportFile
from classes.split_into_tables import SplitIntoNewTables
from classes.filters import Filters
from classes.plotting import Plotting
#end import

#Those three classes are responsible for estabilishing connection with database
database = SqliteDatabase('correlation_dep.db')
database.connect()
    
class BaseModel(Model):
    class Meta():
        database = database
    
class CorellationPolynomial(BaseModel):
    r_squared_poly = DoubleField()
    filter_parameter_poly = FloatField()
 

class CorellationLinear(BaseModel):
    r_squared_lin = DoubleField()
    filter_parameter_lin = FloatField()
#database connected, two tables with columns R^2 and delta_y created   

#next class manipulates (save or get) parameter from database
class ParameterManipulation(object):
    
    def __init__(self):
        pass
    
    def add_value(self, r_squared, filter_parameter):
        added_value = CorellationPolynomial.create(r_squared_poly = r_squared, filter_parameter_poly = filter_parameter)
        print 'value_added_succesfully'
        
    def get_value(self, r_squared):
        rest=2
        for parameters in CorellationPolynomial.select():
            if abs(parameters.r_squared_poly - r_squared) < rest:
                rest = abs(parameters.r_squared_poly - r_squared)
                delta_y_table_value = parameters.filter_parameter_poly
                r_2_table_value = parameters.r_squared_poly
        return r_2_table_value, delta_y_table_value


#executes all commands
class Main(object):

    def __init__(self, data_pathname, Learn):
        self.learn = Learn
        self.data_pathname = data_pathname
        self.parameter_manipulation = ParameterManipulation()
        self.import_file = ImportFile()
        self.split_into_new_tables = SplitIntoNewTables()
        self.filters = Filters()
        self.plotting = Plotting()
        
    def save_data(self):
        Learn = self.learn
        import_file = ImportFile()
        split_into_new_tables = SplitIntoNewTables()
        filters = Filters()
        plotting = Plotting()
        parameter_manipulation = ParameterManipulation()
        
        #applies filters to every file in the directory
        for data_file in os.listdir(self.data_pathname):
            entry_data = import_file.open_file(self.data_pathname + data_file)
            change_number = split_into_new_tables.where_to_split(entry_data)
            for number_1, number_2 in zip(change_number, change_number[1:]):           
                ready_to_analize_array = entry_data[number_1:number_2]   
                column_name = entry_data['f1']
                name = column_name[number_1].split(':', 1)[1]
                array_to_analize = filters.normalize_to_highest_value(ready_to_analize_array)
                evaluation_array = array_to_analize
                time_data_for_zero_point = evaluation_array['f3']
                test_array = array_to_analize
                
                
                print CorellationPolynomial.select().count()              
                r_squared = filters.polynomial_params(array_to_analize)
                if CorellationPolynomial.select().count() == 0:                
                    delta_y_value = 0.4
                    print 'Teach me how to analyze, you have to. mhhhhm'
                else:             
                    r_2_table_value, delta_y_value = parameter_manipulation.get_value(r_squared)
                    print 'found sth!' 
                diff_x, diff_y, diff_outliers, diff_array  = filters.double_subtraction_filter(array_to_analize)
                poly_x, poly_y, x_position, poly_coeff_array = filters.polynomial_filter(array_to_analize, delta_y_value)
                
                #while True:    #Leave like this for normal operation. Delete hash and hash the while below for learning
                while len(set(diff_outliers).intersection(x_position)) != 0:                   
                    print len(diff_outliers), len(x_position), len(array_to_analize), len(set(diff_outliers).intersection(x_position)), '///////'
                    cut_it = []
                    cut_it_debug = []
                    for element in diff_outliers:
                        if element in x_position:     
                            cut_it.append(element)
                    #Below enable for debugging 
                    #print poly_coeff_array
                    #plotting.draw_plot(cut_it, array_to_analize, poly_coeff_array, delta_y_value)
                    if Learn == True:
                        answer = raw_input('is the filtration corect? [y/n]> ')
                    elif Learn == False:
                        answer = 'y'
                    if answer == 'n':
                        print r_squared, delta_y_value
                        delta_y_value = float(raw_input('what dy value would be better?> '))
                        poly_x, poly_y, x_position, poly_coeff_array = filters.polynomial_filter(array_to_analize, delta_y_value)
                    elif answer == 'enough':
                        break
                    elif answer == 'y':
                        while len(cut_it) != 0:                            
                            value = cut_it[-1]                
                            array_to_analize = np.delete(array_to_analize, value, None)
                            cut_it.pop(-1)
                        if Learn == True:    
                            if (CorellationPolynomial.select().where(CorellationPolynomial.r_squared_poly == r_squared).count() == 0):                  
                                parameter_manipulation.add_value(r_squared, delta_y_value)
                        diff_x, diff_y, diff_outliers, diff_array  = filters.double_subtraction_filter(array_to_analize)
                        r_squared = filters.polynomial_params(array_to_analize)
                        r_2_table_value, delta_y_value = parameter_manipulation.get_value(r_squared)
                        poly_x, poly_y, x_position, poly_coeff_array = filters.polynomial_filter(array_to_analize, delta_y_value)
                    else:
                        print 'wrong answer!'
                               
                diff_x, diff_y, diff_outliers, diff_array  = filters.double_subtraction_filter(array_to_analize)
                reglin_x_narrow, reglin_y_narrow, x_position_narrow = filters.linear_regression_filter_narrow_window(array_to_analize)
            
                while len(set(diff_outliers).intersection(x_position_narrow)) != 0:
                    cut_it_narrow = []
                    for element in diff_outliers:
                        if element in x_position_narrow:     
                            cut_it_narrow.append(element)
                            
                    while len(cut_it_narrow) != 0:
                        value = cut_it_narrow[-1]                
                        array_to_analize = np.delete(array_to_analize, value, None)
                        cut_it_narrow.pop(-1)
            
                    array_to_analize = array_to_analize
                    diff_x, diff_y, diff_outliers, diff_array  = filters.double_subtraction_filter(array_to_analize)
                    reglin_x_narrow, reglin_y_narrow, x_position_narrow = filters.linear_regression_filter_narrow_window(array_to_analize)

                diff_x, diff_y, diff_outliers, diff_array  = filters.double_subtraction_filter(array_to_analize)
                reglin_x, reglin_y, x_position = filters.linear_regression_filter_initial_points(array_to_analize)
                while len(set(diff_outliers).intersection(x_position)) != 0:
                    cut_it = []
                    for element in diff_outliers:
                        if element in x_position:     
                            cut_it.append(element)
    
            
                    while len(cut_it) != 0:
                        value = cut_it[-1]                
                        array_to_analize = np.delete(array_to_analize, value, None)
                        cut_it.pop(-1)
                    
                    diff_x, diff_y, diff_outliers, diff_array  = filters.double_subtraction_filter(array_to_analize)
                    reglin_x, reglin_y, x_position = filters.linear_regression_filter_initial_points(array_to_analize)
                         
                array_to_normalize = array_to_analize
                normalizator = filters.check_for_initial_noises(array_to_normalize)
                normalized_array = filters.normalize_to_initial_value(array_to_normalize, normalizator)                
                #For learning hash savetxt below        
                np.savetxt('normalized_'+name+'_'+data_file, normalized_array, fmt='%d, %s, %s, %f, %f, %f, %f, %f, %f, %f', delimiter=',')  
                print name
                if Learn == True:
                    skip_it = raw_input("Do you want to skip this chart plotting? > ")          
                    print skip_it
                    if skip_it == 'no':
                        plotting.draw_plot(cut_it, normalized_array, poly_coeff_array, delta_y) 
                    next_round = raw_input("want to continue? type yes or no. > ")
                    if next_round == 'no':
                        break 
                        
runner = Main('/home/zolw/Documents/Coding/Python/Rera/rera/data_to_normalize/', Learn=False)
runner.save_data()

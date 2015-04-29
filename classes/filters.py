import collections
import numpy as np
import scipy as sp
from scipy import stats

# class containing all used (and unused) filters - reglin, polynomial, single subtraction (name is wrong so far) and normalization methods
class Filters(object):
    
    def __init__(self):
        pass
    
    def linear_regression_filter(self, array_to_analize):
        
        data_for_filtration = array_to_analize['f3']
        time_frame = array_to_analize['f2']
        
        x_positions = []
        reglin_x = []
        reglin_y = []

        for ii in range(0, time_frame.size):
            slope, intercept, r_value, p_value, stderr = sp.stats.linregress(time_frame, data_for_filtration)
                     
            y = (slope*time_frame[ii]) + intercept
            x_0_position = (slope*time_frame[0]) + intercept 
            #if r_value**2 < 0.1:
                #raise ValueError, "Ooops, sth went REALLY wrong with the measurement. Ask your supervisor what are you doing wrong!"
            if r_value**2 > 0.8:
                if ((y+(0.1+stderr)) < data_for_filtration[ii]) or ((y-(0.1+stderr)) > data_for_filtration[ii]): 
                    x_positions.append(ii)
            elif r_value**2 <=0.5:
                if ((y+(0.1+stderr)) < data_for_filtration[ii]) or ((y-(0.1+stderr)) > data_for_filtration[ii]): 
                    x_positions.append(ii)
            elif r_value**2 <=0.62:
                if ((y+(0.45+stderr)) < data_for_filtration[ii]) or ((y-(0.45+stderr)) > data_for_filtration[ii]): 
                    x_positions.append(ii)
            elif r_value**2 <= 0.7:
                if ((y+(0.35+stderr)) < data_for_filtration[ii]) or ((y-(0.35+stderr)) > data_for_filtration[ii]): 
                    x_positions.append(ii)
            elif r_value**2 <= 0.8:
                if ((y+(0.25+stderr)) < data_for_filtration[ii]) or ((y-(0.25+stderr)) > data_for_filtration[ii]): 
                    x_positions.append(ii)
            
        for position in x_positions:
            reglin_x.append(time_frame[position])
            reglin_y.append(data_for_filtration[position])                                    
        
        return reglin_x, reglin_y, x_positions, x_0_position
    
    def linear_regression_filter_narrow_window(self, array_to_analize):
        
        data_for_filtration = array_to_analize['f3']
        time_frame = array_to_analize['f2']
        
        x_positions_narrow = []
        reglin_x_narrow = []
        reglin_y_narrow = []

        for ii in range(25, time_frame.size):
            slope, intercept, r_value, p_value, stderr = sp.stats.linregress(time_frame[ii-25:ii+26], data_for_filtration[ii-25:ii+26])
                                   
            y = (slope*time_frame[ii]) + intercept
            if ((y+(0.1+stderr)) < data_for_filtration[ii]) or ((y-(0.1+stderr)) > data_for_filtration[ii]):
                x_positions_narrow.append(ii)
        for position in x_positions_narrow:
            reglin_x_narrow.append(time_frame[position])
            reglin_y_narrow.append(data_for_filtration[position])                                    
        
        return reglin_x_narrow, reglin_y_narrow, x_positions_narrow
    
    def linear_regression_filter_initial_points(self, array_to_analize):
        
        data_for_filtration = array_to_analize['f3']
        time_frame = array_to_analize['f2']
        
        x_positions = []
        reglin_x = []
        reglin_y = []

        for ii in range(0, 10):
            slope, intercept, r_value, p_value, stderr = sp.stats.linregress(time_frame[0:10], data_for_filtration[0:10])
     
            y = (slope*time_frame[ii]) + intercept
            if r_value**2 < 0.1:
                if ((y+(0.05+stderr)) < data_for_filtration[ii]) or ((y-(0.05+stderr)) > data_for_filtration[ii]): 
                    x_positions.append(ii)  
            elif ((y+(0.15+stderr)) < data_for_filtration[ii]) or ((y-(0.15+stderr)) > data_for_filtration[ii]): 
                    x_positions.append(ii)
                    
        for position in x_positions:
            reglin_x.append(time_frame[position])
            reglin_y.append(data_for_filtration[position])                                    
        
        return reglin_x, reglin_y, x_positions
    
    
    def polynomial_params(self, array_to_analize):
        data_for_filtration = array_to_analize['f3']
        time_frame = array_to_analize['f2']
        
        poly_coeff_array, poly_stats = np.polynomial.polynomial.polyfit(time_frame, data_for_filtration, 3, rcond=None, full=True)        
        #calculate R^2, first total sum of squares
        mean_value = np.mean(data_for_filtration)
        mean_sum = 0
        residual_sum_of_squares = poly_stats[0][0]
        for element in data_for_filtration:
            mean_sum += (element-mean_value)**2
        r_squared = 1-(residual_sum_of_squares/mean_sum)
        
        return r_squared
        
    def polynomial_filter(self, array_to_analize, delta_y):
        
        data_for_filtration = array_to_analize['f3']
        time_frame = array_to_analize['f2']
        x_positions = []
        poly_x = []
        poly_y = []
        
        poly_coeff_array, poly_stats = np.polynomial.polynomial.polyfit(time_frame, data_for_filtration, 3, rcond=None, full=True)        
        #calculate R^2, first total sum of squares
        mean_value = np.mean(data_for_filtration)
        mean_sum = 0
        residual_sum_of_squares = poly_stats[0][0]
        for element in data_for_filtration:
            mean_sum += (element-mean_value)**2
        r_squared = 1-(residual_sum_of_squares/mean_sum)
        
        for ii in range(0, time_frame.size):
            value = data_for_filtration[ii]
            calculated_value = np.polynomial.polynomial.polyval(time_frame[ii], poly_coeff_array)
            #r_2_table_value, delta_y = self.parameter_manipulation.get_value
            if (value > (calculated_value + delta_y)) or (value < (calculated_value - delta_y)):
                x_positions.append(ii)
                        
        for position in x_positions:
            poly_x.append(time_frame[position])
            poly_y.append(data_for_filtration[position])                                    
        
        return poly_x, poly_y, x_positions, poly_coeff_array
                                                    
    #should be single subtraction        
    def double_subtraction_filter(self, array_to_analize):
        
        data_for_filtration = array_to_analize['f3']
        time_frame = array_to_analize['f2']
        diff_array = np.diff(data_for_filtration, n=1)
        diff_outliers = []
        diff_x = []
        diff_y = []
        counter = 0
        for ii, ii_1 in zip(diff_array, diff_array[1:]):
            counter += 1
            if (ii_1 < 0 and ii > 0) or (ii_1 > 0 and ii < 0):
                diff_outliers.append(counter)             
        
        for element in diff_outliers:
            diff_x.append(time_frame[element])
            diff_y.append(data_for_filtration[element])
        return diff_x, diff_y, diff_outliers, diff_array
    
    def check_for_initial_noises(self, array_to_analize):
        data_for_filtration = array_to_analize['f3']
        time_frame = array_to_analize['f2']
        where_to_normalize = []
        
        for ii in range(1, time_frame.size):
            slope, intercept, r_value, p_value, stderr = sp.stats.linregress(time_frame[ii-1:ii+2], data_for_filtration[ii-1:ii+2])
            if r_value**2 > 0.75:                              
                where_to_normalize.append(ii-1)
                break
   
        if len(where_to_normalize) == 0:
            print 'It\'s noisy out here!'
        
        normalizator = data_for_filtration[where_to_normalize[0]]
        return normalizator
                
    def normalize_to_initial_value(self, array_to_normalize, normalizator):    
        data_for_filtration = array_to_normalize['f3']
        time_frame = array_to_normalize['f2']

        counter = 0        
        for element in data_for_filtration:
            data_for_filtration[counter] = element/normalizator
            counter += 1
        normalized_array = array_to_normalize
        return normalized_array   
        
    def normalize_to_highest_value(self, array_to_normalize):    
        data_for_filtration = array_to_normalize['f3']
        time_frame = array_to_normalize['f2']
        
        normalizator = np.max(data_for_filtration)
        counter = 0        
        for element in data_for_filtration:
            data_for_filtration[counter] = element/normalizator
            counter += 1
        normalized_array = array_to_normalize
        return normalized_array   

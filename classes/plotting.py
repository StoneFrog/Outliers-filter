import numpy as np
import matplotlib.pyplot as plt

#class containing method for plotting two graphs at once
class Plotting(object):
    
    def __init__(self):
        pass
   
    def draw_plot(self, cut_points, check_array, poly_coeff_array, delta_y_value):      
        #original_eff = input_array['f3']
        #time_frame = input_array['f2']
        #x = np.linspace(0, time_frame[-1], num=60)
        x_out = []
        y_out = []
        check_eff = check_array['f3']
        check_time = check_array['f2']
        x = np.linspace(0, check_time[-1], num=60)
        
        for position in cut_points:
            x_out.append(check_time[position])
            y_out.append(check_eff[position])
        
        plt.figure(figsize=(12, 6))
        plt.plot()
        plt.scatter(check_time, check_eff, c='#348ABD', label='Filtered')
        plt.scatter(x_out, y_out, c='#E24A33', label='outliers')
        plt.plot(x, np.polynomial.polynomial.polyval(x, poly_coeff_array), c='#E24A33', label='fitcurve')
        plt.plot(x, np.polynomial.polynomial.polyval(x, poly_coeff_array)-delta_y_value, c='yellow', label='upperlim')
        plt.plot(x, np.polynomial.polynomial.polyval(x, poly_coeff_array)+delta_y_value, c='green', label='lowerlim')
        plt.legend()
        #plt.subplot(212)
        #plt.scatter(check_time, check_eff, c='#E24A33', label='Reference')
        #plt.legend()
        plt.show()

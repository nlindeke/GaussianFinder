import data as d
import ticks

import pandas as pd
import numpy as np
import scipy.stats as ss
import matplotlib.pyplot as plt

stocks = list(ticks.symbol_dict)

class cointSeries:
    def __init__(self):
        self.iid = stocks
        self.ts = d.datamanager(self.iid, 2013,1,2017,5).closeData()
        
    def createCoint(self):
        """
        Find the most gaussiany cointegrated pairs
        TODO: Find a better measure for Gaussian-ness
        """
        ts = self.ts
        roll_length = 50
        nof_interation = np.shape(ts)[1]
        global_best = [10, 'nan', 'nan']
        
        for iteration in range(nof_interation):

            score = []

            for i in range(nof_interation):
    
                ma = np.array(ts[self.iid[i]].rolling(window=roll_length).mean().dropna())
                ts_adj = np.array(ts[self.iid[i]])[roll_length-1:]
                weighted_one = ts_adj/ma
    
                ran_choice = int(np.random.choice(len(self.iid), 1))
                if ran_choice == i: ran_choice = int(np.random.choice(len(self.iid), 1))
    
                ma_s = np.array(ts[self.iid[ran_choice]].rolling(window=roll_length).mean().dropna())
                ts_adj_s = np.array(ts[self.iid[ran_choice]])[roll_length-1:]
                
                #TODO: Look for better way of 'normalizing' the time series
                try :
                    weighted_two = ts_adj_s/ma_s
                    
                except ValueError:
                    print("Error occured in the pair: ", self.iid[i], self.iid[ran_choice])
                    continue

                spread = weighted_one - weighted_two  
                kur = ss.kurtosis(spread)
                k = np.corrcoef(np.array(ts[self.iid[i]]), np.array(ts[self.iid[ran_choice]]))

                #If kurtosis and the correlation is positive save the value 
                #otherwise save shit-value so it won't be considered
                if kur > 0.0 and k[1,0] > 0.3:
                    score.append([kur, self.iid[i], self.iid[ran_choice]])
                else:
                    score.append([10, self.iid[i], self.iid[ran_choice]])

            local_best = min(score, key=lambda x: x[0])
            print(global_best)

            #Update global best if a better pair is found
            if local_best[0] < global_best[0]:
                global_best = local_best

        return global_best, [ts[global_best[1]], ts[global_best[2]]]

x = cointSeries().createCoint()
print(x[0])
plt.plot(np.array([x[1][1], x[1][0]]).T)

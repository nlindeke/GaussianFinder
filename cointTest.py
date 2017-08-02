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
        self.ts = d.datamanager(self.iid, 2015,1,2017,1).closeData()
        
    def createCoint(self):
        
        ts = self.ts
        roll_length = 50
        global_best = [10, 'nan', 'nan']
        
        for iteration in range(0,10):

            score = []

            for i in range(np.shape(ts)[1]):
                
    
                ma = np.array(ts[self.iid[i]].rolling(window=roll_length).mean().dropna())
                ts_adj = np.array(ts[self.iid[i]])[roll_length-1:]
                weighted_one = ts_adj/ma
    
                ran_choice = int(np.random.choice(len(self.iid), 1))
                if ran_choice == i: ran_choice = int(np.random.choice(len(self.iid), 1))
    
                ma_s = np.array(ts[self.iid[ran_choice]].rolling(window=roll_length).mean().dropna())
                ts_adj_s = np.array(ts[self.iid[ran_choice]])[roll_length-1:]
                weighted_two = ts_adj_s/ma_s
    
                spread = weighted_one - weighted_two
    
                kur = ss.kurtosis(spread)
                
                if kur > 0:
                    score.append([kur, self.iid[i], self.iid[ran_choice]])
                else:
                    score.append([10, self.iid[i], self.iid[ran_choice]])
            
            local_best = min(score, key=lambda x: x[0])

        if local_best[0] < global_best[0]:
            global_best = local_best
                
        return global_best
            
        
x = cointSeries().createCoint()
print(x)


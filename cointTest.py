import data as d
import ticks

import pandas as pd
import numpy as np
import scipy.stats as ss
import matplotlib.pyplot as plt

stocks = list(ticks.symbol_dict)
etfs = ticks.etf_list
#dat = d.datamanager(etfs, 2012,1,2017,7).closeData()
#dat.to_csv('etf_data', sep=';')

class coint_series:
    def __init__(self):
        self.iid = etfs
        #self.ts = d.datamanager(self.iid, 2013,1,2017,7).closeData()
        self.ts = pd.DataFrame.from_csv('etf_data', sep=';')
        
    def create_coint(self, ll):
        """
        Find the most gaussiany cointegrated pairs
        TODO: Find a better measure for Gaussian-ness  
        """
        ts = self.ts[ll:ll + 300]
        top_players = []        
        roll_length = 100
        nof_interation = np.shape(ts)[1]
        global_best = [100, 'nan', 'nan']
        for iteration in range(nof_interation):

            score = []

            for i in range(nof_interation):
                weighted_one = 0.0
                weighted_two = 0.0
    
                ma = np.array(ts[self.iid[i]].rolling(window=roll_length).mean().dropna())
                ts_adj = np.array(ts[self.iid[i]])[roll_length-1:]
                try:
                    weighted_one = (ts_adj - ma) / np.std(ts_adj)
                except ValueError:
                    #print("Error occured in the pair: ", self.iid[i], self.iid[ran_choice])
                    continue
    
                ran_choice = int(np.random.choice(len(self.iid), 1))
                if ran_choice == i: ran_choice = int(np.random.choice(len(self.iid), 1))
    
                ma_s = np.array(ts[self.iid[ran_choice]].rolling(window=roll_length).mean().dropna())
                ts_adj_s = np.array(ts[self.iid[ran_choice]])[roll_length-1:]
                

                try :
                    weighted_two = (ts_adj_s - ma_s) / np.std(ts_adj_s)
                    
                except ValueError:
                    #print("Error occured in the pair: ", self.iid[i], self.iid[ran_choice])
                    continue

                spread = weighted_one - weighted_two  
                kur = ss.kurtosis(spread)
                k = np.corrcoef(np.array(ts[self.iid[i]]), np.array(ts[self.iid[ran_choice]]))

                #If kurtosis and the correlation is positive save the value 
                #otherwise save shit-value so it won't be considered
                if kur > 0.0 and k[1,0] > 0.3:
                    score.append([kur, self.iid[i], self.iid[ran_choice]])
                else:
                    score.append([100, self.iid[i], self.iid[ran_choice]])

            local_best = min(score, key=lambda x: x[0])
            

            #Update global best if a better pair is found
            if local_best[0] < global_best[0]:
                global_best = local_best
                top_players.append(global_best)

        return global_best, [ts[global_best[1]], ts[global_best[2]]], top_players

    def find_same_in_seq(self):
        """
        Extract the most recurring assets to construct any form of pair.
        """
        seq = []
        score = []
        rng = np.arange(0,1000,100)
        
        for look in rng:
            x = self.create_coint(look)
            for m in range(len(x[2])):
                for k in range(1,3):
                    seq.append(x[2][m][k])    

        for i in range(0, len(seq) - 2, 2):
            pair = seq[i:i+2]
            for k in range(0, len(seq) - 2, 2):
                if k == i: continue
                counter_pair = seq[k:k + 2]
                match = 0
                for m in range(2):
                    if counter_pair[m] == pair[m]:
                        match += 1
                    if m == 1 and counter_pair[m - 1] == pair[m] or counter_pair[m] == pair[m - 1]:
                        match += 1
                    if m == 1 and match > 0:
                        score.append([i, match, k])
                        
        score = [[seq[score[i][0]], seq[score[i][2]]] if score[i][1] >= 2 else 0 for i in range(len(score))]
        return score


    
    




same_seq = coint_series().find_same_in_seq()
print(same_seq)
    
"""
toplist = []
for lookback_length in [300, 500, 700, 900]:
    print("")
    print("Evaluating from 2012 plus {} days".format(lookback_length))
    
    x = cointSeries().createCoint(lookback_length)
    toplist.append(x[2])
    
    one = x[1][1]
    ma = np.array(one.rolling(window=50).mean().dropna())
    ts_adj = np.array(one)[50-1:]
    weighted_one = (ts_adj -ma) / np.std(ts_adj)
    
    two = x[1][0]
    
    ma2 = np.array(two.rolling(window=50).mean().dropna())
    ts_adj2 = np.array(two)[50 - 1:]
    weighted_two = (ts_adj2 -ma2) / np.std(ts_adj2)
    spread = weighted_one - weighted_two
    
    s1 = np.array([weighted_one, weighted_two]).T
    s2 = np.array(spread)
    plt.figure(1)
    plt.subplot(211)
    plt.plot(s1)
    plt.subplot(212)
    plt.plot(s2)
    plt.show()
"""



import pandas_datareader.data as web
import pandas as pd
import datetime as date
from calendar import monthrange

from pandas_datareader import data, wb

class datamanager:

    def __init__(self, iid, startYear, startMonth, endYear, endMonth):
        self.iid = iid
        self.start = date.datetime(startYear, startMonth, 1)
        self.end = date.datetime(endYear, endMonth, monthrange(endYear,endMonth)[1]) 

    def closeData(self):
        key = 'Close'
        bars = data.DataReader(self.iid, "google", self.start, self.end)
        return bars[key]
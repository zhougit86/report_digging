import tushare as ts
import numpy as np

codes = ts.get_stock_basics()
codes = codes.loc['300358':]
# for i in codes/.index:
print np.shape(codes)
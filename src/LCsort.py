import numpy as np
import matplotlib.pyplot as pl

model = np.genfromtxt('/home/blairlm/workspace/RRa1.templ')


              
pl.plot(model[:,0],model[:,1])
pl.title('RR Lyrae Template')
pl.xlabel('Phase')
pl.ylabel('Normalized Magnitude')
pl.xlim([0,1])
pl.ylim([0,-1])
pl.show()
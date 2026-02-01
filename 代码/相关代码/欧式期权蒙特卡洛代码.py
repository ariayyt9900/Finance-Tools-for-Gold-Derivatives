import numpy as np
from numpy.random import standard_normal
def callMonteCarlo(S,X,r,sigma,t,n):
	z=standard_normal(n)
	St=S*np.exp((r-0.5*sigma**2)*t+sigma*z*np.sqrt(t))
	return sum(np.maximum(0,St-X))*(np.exp(-r*t))/n
def putMonteCarlo(S,X,r,sigma,t,n):
	z=standard_normal(n)
	St=S*np.exp((r-0.5*sigma**2)*t+sigma*z*np.sqrt(t))
	return sum(np.maximum(0,X-St))*(np.exp(-r*t))/n
c=callMonteCarlo(5.29,6,0.04,0.24,0.5,100000)  #参数依次为s,k,r,sigma,t,模拟次数n
p=putMonteCarlo(5.29,6,0.04,0.24,0.5,100000)   #参数依次为s,k,r,sigma,t,模拟次数n
print('蒙特卡洛模拟算出的欧式看涨期权价格为{:.4f}'.format(c))
print('蒙特卡洛模拟算出的欧式看跌期权价格为{:.4f}'.format(p))

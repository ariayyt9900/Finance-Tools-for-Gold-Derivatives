import numpy as np
import math
import matplotlib.pyplot as plt
from numba import jit
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #正常显示负号


#生成几何布朗运动
def mcs_simulation(S0,r,b,T,sigma,paths,steps):
    """
    S0:期初价格
    r:折现率
    b:持有成本，b=r就是标准的无股利，b=r-q就是有股利模型
    T：到期期限 
    sigma：波动率 
    paths:路径数（模拟次数）
    steps：模拟天数
    """
    dt = T/steps
    S_path = np.zeros((steps+1,paths))
    S_path[0] = S0
    for step in range(1,steps+1):
        rn = np.random.standard_normal(paths) 
        S_path[step] = S_path[step - 1] * np.exp((b-0.5*sigma**2)*dt +sigma*np.sqrt(dt)*rn) #几何布朗运动的解        
    return S_path
# 计算每条路径的敲入敲出情况，并求期望现金流，得到期权价值
@jit(forceobj = True)  #numba加速计算，会快一些
def auto_callable(S0,r,b,T,sigma,paths,steps,knock_out,knock_in,coupon):  
    """
    knock_out：敲出值
    knock_in：敲入值
    coupon：票息
    """

    S_paths = mcs_simulation(S0,r,b,T,sigma,paths,steps)
    cash_flow = np.zeros(paths)  #用于存储每条路径的现金流

    knock_out_count = 0
    knock_in_count = 0
    not_in_out = 0
    for i in range(paths):  #对每条模拟路径进行循环，分析敲入敲出情况
        knock_out_index = np.where(S_paths[:,i] >= knock_out*S0)[0]  #敲出的index
        knock_out_index = knock_out_index[knock_out_index % 21 ==0] # 简化假设每21个交易日为观察日
        knock_in_index = np.where(S_paths[:,i]< knock_in*S0)[0] #以表现差的确定敲入，相当于有一个敲入就算敲入


        # 1.敲出
        if knock_out_index.size > 0:
            t = knock_out_index[0]  #第一个敲出点
            cash_flow[i] = coupon * t/252 * np.exp(-r * t/252)
            knock_out_count = knock_out_count + 1
        # 2.未敲出也未敲入
        elif knock_out_index.size == 0 and knock_in_index.size == 0:
            cash_flow[i] = coupon*T * np.exp(-r * T)
            not_in_out = not_in_out + 1
        # 3.敲入但未敲出
        elif knock_out_index.size == 0 and knock_in_index.size > 0:
            payoff = min(S_paths[-1][i]/S0-1,0)
            cash_flow[i] =  payoff *np.exp(-r * T)
            knock_in_count = knock_in_count + 1
        else:
            pass

    seneriao_count = {"敲出比率":knock_out_count/paths,"敲入比率":knock_in_count/paths,"未敲入敲出":not_in_out/paths}

    return cash_flow.mean(),seneriao_count #这里减1代表减去本金的净收益
    #S0:期初价格，r:折现率，b:持有成本，b=r就是标准的无股利，b=r-q就是有股利模型，T：到期期限，sigma：波动率（年化），paths:路径数（模拟次数），steps：模拟天数

b=auto_callable(S0=100,r=0.03,b=0.03,T=1,sigma=0.13,paths=500000,steps = 252,knock_out=1.03,knock_in=0.85,coupon=0.2)


print(b)

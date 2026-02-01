import numpy as np
from numpy.random import standard_normal

def Asian_Option(S, K, t, r, sigma,N):             
    """
    S    #标的物现价
    K    #期权行权价格
    t    #到期时间
    r    #无风险年利率
    sigma   #标的物年波动率
    N    #模拟路径数量
    """  
    days=int(t*365)                    #期权剩余天数
    dt=1/365                           #每步为1天
    S_t = np.zeros(days + 1)
    S_t[0] = S                         #标的物现价                      
    M=100000                           #模拟次数
    call_averprice_option=np.array([]) #模拟的平均价格看涨期权价格序列
    put_averprice_option=np.array([])  #模拟的平均价格看跌期权价格序列
    call_averK_option=np.array([])     #模拟的平均执行价格看涨期权价格序列
    put_averK_option=np.array([])      #模拟的平均执行价格看跌期权价格序列
    
    for i in range(1, N + 1):
        W = np.random.normal(0.0, 1.0, (days + 1,))  # 正态分布随机数
        for j in range(1,days+1):
            S_t[j] = S_t[j - 1] * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * W[j])

        once_call_averprice=np.maximum(np.mean(S_t)-K,0)       #单次模拟的期权价格,平均价格看涨期权                     
        once_put_averprice=np.maximum(K-np.mean(S_t),0)        #单次模拟的期权价格,平均价格看跌期权

        once_call_averK=np.maximum(S_t[-1]-np.mean(S_t),0)     #单次模拟的期权价格,平均执行价格看涨期权
        once_put_averK=np.maximum(np.mean(S_t)-S_t[-1],0)      #单次模拟的期权价格,平均执行价格看跌期权

        call_averprice_option = np.append(call_averprice_option,once_call_averprice)  #模拟的平均价格看涨期权价格序列            
        put_averprice_option = np.append(put_averprice_option,once_put_averprice)     #模拟的平均价格看跌期权价格序列
        
        call_averK_option = np.append(call_averK_option,once_call_averK)              #模拟的平均执行价格看涨期权价格序列
        put_averK_option = np.append(put_averK_option,once_put_averK)                 #模拟的平均执行价格看跌期权价格序列

        Asian_call_averprice_option=np.mean(call_averprice_option)*(np.exp(-r*t))
        Asian_put_averprice_option=np.mean(put_averprice_option)*(np.exp(-r*t))

        Asian_call_averK_option=np.mean(call_averK_option)*(np.exp(-r*t))
        Asian_put_averK_option=np.mean(put_averK_option)*(np.exp(-r*t))

    return Asian_call_averprice_option,Asian_put_averprice_option,Asian_call_averK_option,Asian_put_averK_option

    
 
# 无红利亚式期权，使用示例 
S = 100
K = 100
t = 0.5
r = 0.05
sigma = 0.2
N=1000

call_averprice_option,put_averprice_option,call_averK_option,put_averK_option=Asian_Option(S, K, t, r, sigma, N)
 
 
print(f"亚式平均价格看涨期权价格: {call_averprice_option}")
print(f"亚式平均价格看跌期权价格: {put_averprice_option}")
print(f"亚式平均执行价格看涨期权价格: {call_averK_option}")
print(f"亚式平均执行价格看跌期权价格: {put_averK_option}")

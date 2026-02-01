import numpy as np
from numpy.random import standard_normal

def Asian_Option(S, K, t, r, sigma,start,end,N):             
    """
    S    #标的物现价
    K    #期权行权价格
    t    #到期时间(年）
    r    #无风险年利率
    sigma   #标的物年波动率
    start:回溯起始时间距离期权到期日的天数
    end:回溯结束时间距离期权到期日的天数    
    N    #模拟路径数量
    """  
    days=int(t*365)                    #期权剩余天数
    backdpriod=[days-start,days-end]   #回溯时段
    dt=1/365                           #每步为1天
    S_t = np.zeros(days + 1)
    S_t[0] = S                         #标的物现价                      
    M=100000                           #模拟次数
    call_FixStrike_option=np.array([])       #模拟的固定行权价看涨期权价格序列
    put_FixStrike_option=np.array([])        #模拟的固定行权价看跌期权价格序列    
    call_FloatStrike_option=np.array([])     #模拟的浮动行权价看涨期权价格序列
    put_FloatStrike_option=np.array([])     #模拟的浮动行权价看跌期权价格序列
    
    for i in range(1, N + 1):
        W = np.random.normal(0.0, 1.0, (days + 1,))  # 正态分布随机数
        for j in range(1,days+1):
            S_t[j] = S_t[j - 1] * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * W[j])

        Lookback_S_t=S_t[days-start:days-end+1]   #回溯时段标的物价格序列
        Lookback_max=Lookback_S_t.max()           #回溯时段标的物价格最大值
        Lookback_min=Lookback_S_t.min()           #回溯时段标的物价格最小值
                  
        once_call_FixStrike=np.maximum(Lookback_max-K,0)       #单次模拟的期权价格,固定行权价看涨期权                     
        once_put_FixStrike=np.maximum(K-Lookback_max,0)        #单次模拟的期权价格,固定行权价看跌期权

        once_call_FloatStrike=np.maximum(S_t[-1]-Lookback_min,0)     #单次模拟的期权价格,浮动行权价看涨期权
        once_put_FloatStrike=np.maximum(Lookback_min-S_t[-1],0)      #单次模拟的期权价格,浮动行权价看跌期权


        call_FixStrike_option = np.append(call_FixStrike_option,once_call_FixStrike)  #模拟的固定行权价看涨期权价格序列            
        put_FixStrike_option = np.append(put_FixStrike_option,once_put_FixStrike)     #模拟的固定行权价看跌期权价格序列
        
        call_FloatStrike_option = np.append(call_FloatStrike_option,once_call_FloatStrike)              #模拟的浮动行权价看涨期权价格序列
        put_FloatStrike_option = np.append(put_FloatStrike_option,once_put_FloatStrike)                 #模拟的浮动行权价看跌期权价格序列

        Lookback_call_FixStrike_option=np.mean(call_FixStrike_option)*(np.exp(-r*t))
        Lookback_put_FixStrike_option=np.mean(put_FixStrike_option)*(np.exp(-r*t))

        Lookback_call_FloatStrike_option=np.mean(call_FloatStrike_option)*(np.exp(-r*t))
        Lookback_put_FloatStrike_option=np.mean(put_FloatStrike_option)*(np.exp(-r*t))

    return Lookback_call_FixStrike_option,Lookback_put_FixStrike_option,Lookback_call_FloatStrike_option,Lookback_put_FloatStrike_option

    
 
# 无红利回朔期权，使用示例 
S = 100
K = 100
t = 0.5
r = 0.05
sigma = 0.2
start=20
end=10
N=1000

call_averprice_option,put_averprice_option,call_averK_option,put_averK_option=Asian_Option(S, K, t, r, sigma,start,end,N)
 
 
print(f"固定行权价回溯看涨期权价格: {call_averprice_option}")
print(f"固定行权价回溯跌期权价格: {put_averprice_option}")
print(f"浮动行权价回溯看涨期权价格: {call_averK_option}")
print(f"浮动行权价格看跌期权价格: {put_averK_option}")

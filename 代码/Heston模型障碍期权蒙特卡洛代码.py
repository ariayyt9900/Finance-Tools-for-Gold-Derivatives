import numpy as np  
from scipy.stats import norm  
  
def heston_process(S0, V0, kappa, theta, sigma, rho, r, T, dt, N):  
    """  
    模拟Heston过程  
    参数:  
        S0: 初始股票价格  
        V0: 初始波动率  
        kappa: 波动率均值回复速度  
        theta: 长期波动率水平  
        sigma: 波动率的波动率  
        rho: 股票价格和波动率之间的相关系数  
        r: 无风险利率  
        T: 总时间  
        dt: 时间步长  
        N: 模拟路径数  
    返回:  
        股票价格路径和波动率路径  
    """  
    dt_sqrt = np.sqrt(dt)  
    t = np.arange(0, T + dt, dt)  
    S = np.zeros((N, len(t)))  
    V = np.zeros((N, len(t)))  
    Z1 = np.random.randn(N, len(t) - 1)  
    Z2 = np.random.randn(N, len(t) - 1)  
      
    S[:, 0] = S0  
    V[:, 0] = V0  
      
    for i in range(1, len(t)):  
        dV = kappa * (theta - V[:, i-1]) * dt + sigma * np.sqrt(V[:, i-1]) * Z1[:, i-1] * dt_sqrt  
        dS = r * S[:, i-1] * dt + np.sqrt(V[:, i-1]) * S[:, i-1] * (rho * Z1[:, i-1] + np.sqrt(1 - rho**2) * Z2[:, i-1]) * dt_sqrt  
        V[:, i] = V[:, i-1] + dV  
        S[:, i] = S[:, i-1] + dS  
      
    return S, V  
  
def monte_carlo_barrier_option(S0, V0, kappa, theta, sigma, rho, r, T, dt, N, K, B, option_type):  
    """  
    使用蒙特卡洛模拟计算障碍期权价格  
    参数:  
        S0, V0, kappa, theta, sigma, rho, r, T, dt, N: 与heston_process中的参数相同  
        K: 行权价格  
        B: 障碍水平  
        option_type: 'up' 或 'down'，表示上障碍或下障碍期权  
    返回:  
        障碍期权价格  
    """  
    S, V = heston_process(S0, V0, kappa, theta, sigma, rho, r, T, dt, N)  
    payoff = np.zeros(N)  
      
    if option_type == 'up':  
        for i in range(N):  
            if np.max(S[i, :]) < B:  # 如果股票价格从未超过障碍水平  
                if S[i, -1] > K:  # 如果到期时股票价格高于行权价格  
                    payoff[i] = S[i, -1] - K  
    elif option_type == 'down':  
        for i in range(N):  
            if np.min(S[i, :]) > B:  # 如果股票价格从未低于障碍水平  
                if S[i, -1] > K:  # 如果到期时股票价格高于行权价格  
                    payoff[i] = S[i, -1] - K  
    else:  
        raise ValueError("Invalid option_type. Must be 'up' or 'down'.")  
      
    option_price = np.exp(-r * T) * np.mean(payoff)  
    return option_price  
  


import math
from math import sqrt
import matplotlib.pyplot as plt
import numpy as np

# s - stock price
# t - time til maturity
# K - strike
# vol - volatility parameter (sigma)
# r - interest rate
# n - approximation steps
def P(s, t, K, vol, r, n):
    dt = t/n                       # timestep
    u = math.e**(vol * sqrt(dt))   # multiplicative factor
    d = 1/u                        # "
    p = (1 + r*dt - d)/(u-d)       # prob. of upstep
    beta = math.e**(-r * dt)       # interest rate per time period

    bdy = {}
    
    V_kp1 = []
    for k in range(n, -1, -1):
        print("Calculating step ", k)
        V_k = []
        for i in range(0, k+1):
            exer = max(K - s * (u**i * d**(k-i)), 0) # payout if exercised now
            if len(V_kp1) != 0:
                ev_hold = beta * (p * V_kp1[i+1] + (1-p) * V_kp1[i])
            else:
                ev_hold = 0
                
            print(i, " ", "Exercise ev:", exer, " ", "Hold ev:", ev_hold)
            # in this direction, at some point, it becomes better to hold

            if k not in bdy and ev_hold >= exer:
                bdy[k] = s * u**i * d**(k-i)
            
            V_k.append(max(exer, ev_hold))


            
        V_kp1 = V_k[:]

    return V_kp1[0],bdy

def main():
    t = 0.5
    n = 5000
    price, bdy = P(s=51, t=t, K=53, vol=0.32, r=0.05, n=n)

    T = np.linspace(0.0, t, n+1)
    b = dict(sorted(bdy.items()))
    b = list(b.values())
    plt.plot(T, b)
    plt.show()


if __name__ == "__main__":
    main()

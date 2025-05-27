import math
from math import sqrt, exp
import matplotlib.pyplot as plt
import numpy as np

def put(s,t,K,vol,r,n):
    dt = t/n
    u = exp(vol * sqrt(dt))
    d = 1/u
    p = (1 + r*dt - d)/(u-d)
    beta = exp(-r * dt)

    Z = np.zeros(n+1)
    # time n prices
    payouts = np.fromiter(
        [ max(0, K - s * u**i * d**(n-i)) for i in range(0, n+1) ],
        dtype=np.longdouble
    )

    bdy = []

    for k in range(n-1, -1, -1):
        exer_payouts = K + ((payouts-K)/d)
        hold_payouts = beta * ((1-p) * payouts[:-1] + p * payouts[1:])
        
        payouts = np.maximum(exer_payouts[:-1], hold_payouts)

        indicator = (exer_payouts[:-1] >= hold_payouts).astype(int)
        zindex = np.where(indicator == 0)[0]
        zindex = zindex[0] if len(zindex) > 0 else -1
        bdy.append(zindex)

    bdy = np.flip(bdy)
    bdy_prices = [ s * u**i * d**(k-i) for k,i in enumerate(bdy) ]
    print(payouts)
    # print(bdy_prices)
    # T = np.linspace(0.0, t, n)
    # plt.plot(T, bdy_prices)
    # plt.show()


def main():
    put(s=9, t=0.25, K=10, vol=0.3, r=0.06, n=5000)
    
    #price, bdy = P(s=51, t=0.5, K=53, vol=0.32, r=0.05, n=10000)
    #print(price)
    #print(price)

    
    # b = list(b.values())
    # plt.plot(T, b)
    # plt.show()


if __name__ == "__main__":
    main()


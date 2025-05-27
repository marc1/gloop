from math import sqrt, exp

import numpy as np
import matplotlib.pyplot as plt

"""
American put option pricing algorithm using a binomial tree model

Parameters:
s: initial stock price
t: time to maturity
K: strike price
vol: Volatility
r: risk-free interest rate
n: number of timesteps
"""
def P(s, t, K, vol, r, n):
    dt = t/n                      # \Delta
    u = exp(vol * sqrt(dt))       # Multiplier if "up"
    d = 1/u                       # Multiplier if "down"
    p = (1+r*dt - d)/(u-d)        # Probability of "up"
    beta = exp(-r * dt)           # Discount rate per timestep

    # Share prices at maturity
    S_t = np.fromiter(
        [ s * (u**i) * (d**(n-i)) for i in range(0, n+1) ],
        dtype=np.longdouble
    )
    # Payouts at maturity
    payouts = np.maximum(0, K - S_t)

    # For each timestep, the indices of the node (and its corresponding price)
    # at which it is more favorable to hold the option than to exercise it
    bdy_prices = np.zeros(n, np.float32)

    # Inductively populate values of the "binomial tree"
    for k in range(n-1, -1, -1):
        # The share prices at time k are the same as time t prices
        # divided by the number of steps backward.
        S_k = S_t[:-(n-k)]/d**(n-k)

        # Payouts at each node if the owner were to exercise immediately
        exercise_payouts = np.maximum(0, K - S_k)

        # Expected payouts computed recursively from the (k+1)-th timestep 
        hold_payouts = beta * (p * payouts[1:] + (1-p) * payouts[:-1])

        # update payouts based on optimal policy
        payouts = np.maximum(exercise_payouts, hold_payouts)

        # 0 for hold. 1 for exercise.
        exercise_indicator = (exercise_payouts > hold_payouts).astype(int)
        # indices where one should exercise
        exercise_indices = np.where(exercise_indicator == 1)[0]

        if len(exercise_indices) > 0:
            # largest share price to exercise at
            idx = exercise_indices[-1]
            bdy_prices[k] = S_k[idx]
        else:
            # The owner should not exercise at any share price
            bdy_prices[k] = np.nan



    print(payouts)

    T = np.linspace(0.0, t, n)
    valid_indices = ~np.isnan(bdy_prices)
    plt.plot(T[valid_indices], bdy_prices[valid_indices], 'b-', linewidth=1.5)
    plt.grid(True, alpha=0.3)
    plt.xlabel('Time to maturity (years)')
    plt.ylabel('Share price ($)')
    plt.title(f"Optimal exercise boundary for American put option\n$s = {s}$, \
    $t = {t}$, $K={K}$, $\\sigma = {vol}$, $r={r}$, at $n={n:,}$ iterations.")
    plt.show()

def main():
    P(s=223, t=0.5, K=230, vol=0.28, r=0.04, n=20000)

    
if __name__ == "__main__":
    main()    

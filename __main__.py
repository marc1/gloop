import math
import matplotlib.pyplot as plt

# GOAL: Solve for V_0(0)

# helper function to calculate stock price dictionary at time 'k' given 'i' jumps where i ranges (0, k) inclusive
def stock_price_n(s, n, u, d):
    
    time_n_prices = {}
    for i in range(0, n+1):
        s_k = (u**i) * (d**(n-i)) * (s) 
        time_n_prices[i] = round(s_k, 3)

    return time_n_prices

# helper function to compute payout of put at time n, either equal to 0 or K - (stock price) <-> equivalent to finding V_n(i) where i ranges (0, k) inclusive
def put_payouts_n(n, time_k_stock, K):

    time_n_payout = {}
    for i in range(0, n+1):
        time_n_payout[i] = round(max(0, K - time_k_stock[i]), 3)

    return time_n_payout

# algo: V_k(i) = max(K - u^i d^(k - i)s, Beta * p_up * V_(k+1)(i + 1) + Beta * (1 - p_up) * V_(k+1)(i + 1))
def backwards_iteration_payouts(s, n, payouts, K, beta, u, d, p_up, p_down):

    # at each n value, there is a level (i?) where it becomes better to hold the option than to exercise it

    # payouts are as of time n for the first iteration, then reference earlier computations throughout remainder of loops
    time_k_payout = {}
    hold_integers = {}

    for n_iter in range(n-1, 0, -1):
        for i in range(0, n_iter+1):

            # uses payouts from leafs nodes in the first loop
            if n_iter == (n-1):
                exercise_payout = (K - ((u**i) * (d**(n_iter-i)) * (s)))
                expected_return = (beta)*(p_up)*(payouts[i+1]) + (beta)*(p_down)*(payouts[i])
                time_k_payout[n_iter, i] = round(max(exercise_payout, expected_return), 3)

                if (expected_return > exercise_payout) & (n_iter not in hold_integers.keys()):
                    hold_integers[n_iter] = i

            else:
                exercise_payout = (K - ((u**i) * (d**(n_iter-i)) * (s)))
                expected_return = (beta)*(p_up)*(time_k_payout[(n_iter + 1), i+1]) + (beta)*(p_down)*(time_k_payout[(n_iter + 1), i])
                time_k_payout[n_iter, i] = round(max(exercise_payout, expected_return), 3)

                if (expected_return > exercise_payout) & (n_iter not in hold_integers.keys()):
                    hold_integers[n_iter] = i

    
    # extract final two time 1 payouts required to calculate V_0(0)
    V_10 = time_k_payout[(1, 0)]
    V_11 = time_k_payout[(1, 1)]
    put_price = round(max((K - s), beta*(p_up)*V_11 + beta*(p_down)*V_10), 3)

    return put_price, hold_integers

def graph_thresholds(s, u, d, holds_thresholds):
    s_0 = s
    stock_prices = []

    for key, value in holds_thresholds.items():
        mature_price = s_0 * (u**value) * (d**(key - value))
        stock_prices.append(mature_price)

    plt.plot(range(1, len(stock_prices)+1), stock_prices)
    plt.show()

def solve(s, t, K, sig, r, n):

    # Define Parameters Required for 
    delta = round(t/n, 4)
    u = round(math.e**(sig * math.sqrt(delta)), 4)
    d = round(math.e**(-sig * math.sqrt(delta)), 4)
    p_up = round((1 + r*delta - d)/(u-d), 4)
    p_down = round((1 - p_up), 4)
    beta = round(math.e**(-r * delta), 4)
    
    # Returns prices at time n, followed by put payouts at time n (first step of the algo.), the run algo.
    time_n_prices = stock_price_n(s, n, u, d)
    time_n_payouts = put_payouts_n(n, time_n_prices, K)
    put_price = backwards_iteration_payouts(s, n, time_n_payouts, K, beta, u, d, p_up, p_down)[0]
    hold_thresholds = backwards_iteration_payouts(s, n, time_n_payouts, K, beta, u, d, p_up, p_down)[1]

    print(put_price)
    graph_thresholds(s, u, d, hold_thresholds)


def main():
    solve(9, 1/4, 10, 0.3, 0.06, 10)


if __name__ == "__main__":
    main()
import math
from math import sqrt, exp
import matplotlib.pyplot as plt
import numpy as np

def put(s, t, K, vol, r, n):
    """
    American put option pricing using optimized binomial tree model
    
    Parameters:
    s: initial stock price
    t: time to maturity in years
    K: strike price
    vol: volatility
    r: risk-free interest rate
    n: number of time steps
    """
    # Use the Cox-Ross-Rubinstein parameterization for better stability
    dt = t/n
    u = exp(vol * sqrt(dt))
    d = 1/u
    # Risk-neutral probability
    p = (1+r*dt - d)/(u-d)#(exp(r * dt) - d) / (u - d)
    beta = exp(-r * dt)
    
    # Initialize arrays to store option values and boundary prices
    bdy_indices = np.zeros(n, dtype=int)
    bdy_prices = np.zeros(n, dtype=np.longdouble)
    
    # Calculate terminal payoffs at maturity (time step n)
    # Note: At each step j, stock price = s * u^(j-i) * d^i 
    # where i goes from 0 to j (representing up and down movements)
    S = np.zeros(n+1, dtype=np.float64)
    for i in range(n+1):
        S[i] = s * (u ** i) * (d ** (n-i))
    
    # Terminal payoffs
    payouts = np.maximum(0, K - S)
    
    # Work backwards through the tree
    for k in range(n-1, -1, -1):
        # Stock prices at current time step (from lowest to highest)
        S_current = np.zeros(k+1, dtype=np.float64)
        for i in range(k+1):
            S_current[i] = s * (u ** i) * (d ** (k-i))
        
        # Calculate exercise values
        exercise_values = np.maximum(0, K - S_current)
        
        # Calculate continuation values 
        continuation_values = beta * (p * payouts[:-1] + (1-p) * payouts[1:])
        
        # Determine whether to exercise
        payouts = np.maximum(exercise_values, continuation_values)
        
        # Find exercise boundary for visualization
        exercise_indicator = (exercise_values > continuation_values).astype(int)
        
        # For American puts, we want to find the highest stock price where exercise is optimal
        # This is typically the first index (from low to high stock prices) where exercise is no longer optimal
        exercise_indices = np.where(exercise_indicator == 1)[0]
        
        if len(exercise_indices) > 0:
            # Get the highest index where exercise is optimal
            boundary_idx = exercise_indices[-1]
            bdy_indices[k] = boundary_idx
            bdy_prices[k] = S_current[boundary_idx]
        else:
            # No exercise at this time step
            bdy_indices[k] = -1
            bdy_prices[k] = np.nan
    
    # Option price is the value at the root of the tree
    option_price = payouts[0]
    
    # Plot the exercise boundary
    T = np.linspace(0.0, t, n)
    plt.figure(figsize=(10, 6))
    # Filter out NaN values for a cleaner plot
    valid_indices = ~np.isnan(bdy_prices)
    plt.plot(T[valid_indices], bdy_prices[valid_indices], 'b-', linewidth=1.5)
    plt.grid(True, alpha=0.3)
    plt.xlabel('Time to Maturity (years)')
    plt.ylabel('Stock Price ($)')
    plt.title('American Put Option Exercise Boundary')
    plt.show()
    
    return option_price, bdy_prices

def analyze_convergence(s, t, K, vol, r, n_values):
    """
    Analyze how the option price converges as n increases
    """
    prices = []
    for n in n_values:
        price, _ = put(s, t, K, vol, r, n)
        prices.append(price)
        print(f"n = {n}, price = {price}")
    
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, prices, 'ro-')
    plt.grid(True, alpha=0.3)
    plt.xlabel('Number of Time Steps (n)')
    plt.ylabel('Option Price ($)')
    plt.title('American Put Option Price Convergence')
    plt.show()
    
    return prices

def main():
    # Base parameters
    s = 51    # Stock price
    t = 0.5   # Time to maturity (years)
    K = 53    # Strike price
    vol = 0.32  # Volatility
    r = 0.05   # Risk-free rate
    
    # Price with optimized method
    price, boundary = put(s, t, K, vol, r, n=10000)
    print(f"Option price: ${price:.4f}")
    
    # Analyze convergence (optional)
    # n_values = [100, 200, 500, 1000, 2000, 5000, 10000]
    # analyze_convergence(s, t, K, vol, r, n_values)

if __name__ == "__main__":
    main()

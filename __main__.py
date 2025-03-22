import math

def solve(s, t, K, sig, r, n):
    delta = t/n
    beta = math.e**(-r * delta)
    u = math.e**(sig * math.sqrt(delta))
    d = 1/u
    p_up = ((1/beta) - d)/(u-d)

    #j = number of ups
    for j in range(0, n+1):
        print(s * u**j * d**n-j)
    

def main():
    solve(51, 1/2, 53, 0.32, 0.05, 2)

if __name__ == "__main__":
    main()

import numpy as np
# Making an options pricer using the Monte Carlo Simulation

"""
This is the simulation of the geometric brownian motion function.
S0: initial stock price
r: risk-free rate
sigma: volatility
T: time to maturity in years
N: Number of time steps
M: Number of simulation paths

Return: np.ndarray of shape M, N+1 containing the simulated paths
"""
def simulate_gbm_path(S0, r, sigma, T, N, M):
    dt = T / N
    paths = np.zeros((M, N + 1)) # Makes arrays of a given shape and type filled with zeros currently
    paths[:, 0] = S0 # Initialize each path with the starting price of given stock

    drift = (r - .5 * sigma ** 2) * dt
    diffusion = sigma * np.sqrt(dt) # Don't get a Z yet b/c it need to be random for each step and each array.

    for t in range(1, N + 1): 
        Z = np.random.standard_normal(M) # One Z per path at each time step
        paths[:, t] = paths[:, t - 1] * np.exp(drift + diffusion * Z)

    return paths

"""
paths: the simulated brownian paths from the first function
K: strike price
r: risk-free rate
T: time to expiry in years
"""
def price_option(paths, K, r, T, option_type='Call'):
    ST = paths[:, -1] # ST is the unique price of each path at the terminal time step of the simulation
    
    if option_type == 'Call':
        # Numpy vectorization allows you perform all of these operations in parallel on the entire vector
        payoffs = np.maximum(ST - K, 0) # Determining if the call has value
    elif option_type == 'Put':
        payoffs = np.maximum(K - ST, 0) # Determining if the put has value
        
    discounted_payoff = np.exp(-r * T) * payoffs # The discounted payoff of each respective path
    price = np.mean(discounted_payoff) # Averaging the entire vector of payoffs
    return price, payoffs, discounted_payoff
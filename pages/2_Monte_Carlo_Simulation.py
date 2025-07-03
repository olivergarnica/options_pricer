import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from monte_carlo import simulate_gbm_path, price_option

st.set_page_config(layout='wide')
st.title('Monte Carlo Simulation for Pricing Options')

# Inputs
S = st.number_input("Underlying Stock Price (S)", value=100.0)
K = st.number_input("Strike Price (K)", value=100.0)
T = st.number_input("Time to Expiration (T in years)", value=1.000, min_value=0.001, max_value=3.000)
r = st.number_input("Risk-Free Rate (r)", value=0.0434, step=.0001, format="%.4f")
sigma = st.number_input("Implied Volatility (σ)", value=0.2)
# Number of steps first is set to 1 per day
N = st.number_input("Number of steps (N)", value=int(T*252), min_value=1, max_value=int(252*T*3))
M = st.number_input("Number of simulation paths (M)", value = 50, min_value=50, max_value=1000) 

option_type = st.selectbox("Option Type", ["Call", "Put"])

if st.button("Run Monte Carlo Simulation"):
    paths = simulate_gbm_path(S, r, sigma, T, N, M)
    price, payoffs, discounted_payoffs = price_option(paths, K, r, T, option_type)

    # Sim Results Plot
    st.subheader("Simulated Price Paths")
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    for i in range(min(100, M)): 
        ax1.plot(paths[i], alpha=0.5, linewidth=0.5)
    ax1.set_title("Simulated Stock Price Paths")
    ax1.set_xlabel("Time Step")
    ax1.set_ylabel("Price")
    st.pyplot(fig1)

    # Convergence Plot
    st.subheader("Convergence of Monte Carlo Estimate")

    # Creates a vector with 20 MC Sims ranging from 10 to M, and compares how their pricing would be. 
    sample_sizes = np.linspace(10, M, 40, dtype=int)
    convergence = [
        np.mean(np.exp(-r * T) * np.maximum(paths[:m, -1] - K, 0)) if option_type == 'Call'
        else np.mean(np.exp(-r * T) * np.maximum(K - paths[:m, -1], 0))
        for m in sample_sizes
    ]
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.plot(sample_sizes, convergence, marker='o', linestyle='-', linewidth=1)
    ax2.axhline(price, color='red', linestyle='--', label='Final Estimate')
    ax2.set_title("Convergence of Option Price Estimate")
    ax2.set_xlabel("Number of Simulated Paths")
    ax2.set_ylabel("Estimated Option Price")
    ax2.legend()
    st.pyplot(fig2)

    # Final Stock Price Distribution
    st.subheader("Distribution of Terminal Stock Prices")
    fig3, ax3 = plt.subplots(figsize=(10, 4))
    sns.histplot(paths[:, -1], bins=50, kde=True, ax=ax3)
    ax3.set_title("Distribution of Final Stock Prices")
    ax3.set_xlabel("Stock Price at Expiration")
    ax3.set_ylabel("Frequency")
    st.pyplot(fig3)

    # 95% CI for Price
    mean_payoff = np.mean(discounted_payoffs)
    std_error = np.std(discounted_payoffs) / np.sqrt(M)
    # z = 1.96 for a 95% confidence level under the std. normal distribution
    ci_lower = mean_payoff - 1.96 * std_error
    ci_upper = mean_payoff + 1.96 * std_error

    st.subheader("Estimated Option Price")
    # Shows the value to 2 decimal points
    st.metric(label="Option Price", value=f"${price:.2f}")
    st.markdown(f"**95% Confidence Interval:** \\${ci_lower:.2f} to \\${ci_upper:.2f}")

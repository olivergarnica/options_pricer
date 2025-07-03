import streamlit as st

st.title("PRICE THIS OPTION!")
st.markdown("""
Welcome to the home page of the options pricing website. Here contains the various different ways to price options.
The bottom of the page sends you to the various options pricing pages with their interactions.\n\n 
""")

st.markdown("""
## The Black-Scholes Model:\n
The Black-Scholes Model is a mathematical framework for pricing **European-style options**—those that can **only be exercised at expiration**. 
Although it strictly applies to European options, it is still widely used for **American call options on non-dividend-paying stocks**, where early exercise isn’t optimal. 
For more complex situations (e.g., American puts or dividend-paying stocks), other models like **binomial trees**, **Monte Carlo simulations**, or the **Barone-Adesi–Whaley model** may be more appropriate.
""")

st.markdown("### Key Variables")
st.markdown("""
- **S**: Current price of the underlying stock  
- **K**: Strike price — the price at which the option allows you to buy/sell  
- **T**: Time to expiration (in years)  
- **r**: Risk-free interest rate (e.g., 10-year Treasury yield)  
- **σ (volatility)**: Standard deviation of stock returns  
- **N(x)**: CDF of the standard normal distribution — interpreted as probabilities under a risk-neutral framework
""")

st.markdown("### Black-Scholes Formulas")

st.latex(r"d_1 = \frac{\ln(S/K) + (r + \frac{\sigma^2}{2})T}{\sigma \sqrt{T}}")
st.markdown("**d₁ Interpretation:** Standardized z-score measuring how far above or below the strike the expected stock price is.")

st.latex(r"d_2 = d_1 - \sigma \sqrt{T}")
st.markdown("**d₂ Interpretation:** Risk-neutral probability that the option finishes in-the-money.")

st.latex(r"C = S N(d_1) - K e^{-rT} N(d_2)")
st.markdown("**Call price:** Present value of expected payoff under the risk-neutral measure.")

st.latex(r"P = K e^{-rT} N(-d_2) - S N(-d_1)")
st.markdown("**Put price:** Opposite payoff structure, benefits when stock is below strike.")

st.markdown("### Variable Effects on Option Price")
st.markdown("Assume the given variable increases")
st.table({
    "Variable": ["S (Stock Price)", "K (Strike Price)", "T (Time)", "σ (Volatility)", "r (Risk-Free Rate)"],
    "Call Price": ["↑", "↓", "↑", "↑", "↑"],
    "Put Price": ["↓", "↑", "↑", "↑", "↓"],
})
st.markdown("Note: Were you to assume the given variables decrease the directions for the options gets flipped.")

st.markdown("### How to Use")
st.markdown("""
Choose a stock on the yahoo (or any) options chain
Plug in the variables given there on the Black-Scholes Page.
Calculate the price of the call and put.
Mess with the sliders or the price payed for the option to interact with the heatmap and PnL charts. 
""")

st.markdown("### Important Notes")
st.markdown("""
- As very deep ITM or OTM options get near expiry, the IV of the option may be unreasonably large, you can input any large IV and the option would be priced within a few cents. The option becomes almost entirely based on its intrinsic value. We reccomend calculating options that are almost At the Money (ATM).
- Assumes constant volatility and interest rates  
- No arbitrage or transaction costs  
- Stock prices follow a log-normal distribution  
- The model outputs theoretical fair value, not market price
- Greeks (Δ, Γ, Θ, Vega, Rho) measure sensitivities and can be derived from these formulas
""")

st.markdown("""
## The Monte Carlo Simulation

Monte Carlo simulation is a technique used to estimate option prices by simulating many possible future price paths of the underlying asset. It is especially useful for complex or path-dependent options where analytical formulas (like Black-Scholes) fall short.

It works by:
1. Simulating thousands of potential stock price paths using Geometric Brownian Motion.
2. Calculating the payoff for each path at expiration.
3. Discounting those payoffs back to today.
4. Averaging all discounted payoffs to get an estimate of the option's fair value.
""")

st.markdown("### Key Inputs and Parameters")
st.markdown("""
- **S**: Current stock price  
- **K**: Strike price  
- **T**: Time to expiration (in years)  
- **r**: Risk-free interest rate  
- **σ (volatility)**: Annualized standard deviation of returns  
- **N**: Number of time steps per path (e.g., 252 for daily steps in 1 year)  
- **M**: Number of simulated paths (more paths = better accuracy)  
""")

st.markdown("### Geometric Brownian Motion (GBM) Formula")

st.latex(r"S_{t+1} = S_t \cdot e^{(r - \frac{1}{2}\sigma^2)\Delta t + \sigma \sqrt{\Delta t} \cdot Z_t}")
st.markdown("""
This formula drives the simulated price paths.  
- \( Z_t \sim \mathcal{N}(0,1) \): a random standard normal value  
- \( \Delta t = T/N \): time increment  
""")

st.markdown("### Monte Carlo Option Pricing Formula")

st.latex(r"\text{Option Price} = e^{-rT} \cdot \frac{1}{M} \sum_{i=1}^{M} \text{Payoff}_i")
st.markdown("""- For a **Call Option**:""")
st.latex(r"\text{Payoff}_i = \max(S_T^i - K, 0)")
st.markdown("""- For a **Put Option**:""")
st.latex(r"\text{Payoff}_i = \max(K - S_T^i, 0)")
st.markdown("""- Each payoff is discounted using \( e^{-rT} \), assuming risk-neutral pricing.""")


st.markdown("### Why It Works")

st.markdown("""
Monte Carlo works thanks to the Law of Large Numbers — the average of many simulated outcomes converges to the expected value.

Unlike Black-Scholes, which assumes a perfect market and simple payoffs, Monte Carlo simulation:
- Can handle path-dependent options (the assets trajectory through time)
- Is flexible and intuitive but computationally expensive
""")

st.markdown("### Limitations")
st.markdown("""
- Slow convergence; requires many simulations for accuracy  
- Results depend on random seed and quality of simulation  
- Not ideal for American-style options unless combined with specialized methods (e.g., Least Squares Monte Carlo)
""")

if st.button("Go to Black-Scholes Pricer"):
    st.switch_page("pages/1_Black_Scholes_Pricer.py")

if st.button("Go to Monte Carlo Simulation"):
    st.switch_page("pages/2_Monte_Carlo_Simulation.py")
import streamlit as st
from black_scholes import BlackScholes
import pandas as pd
import numpy as np

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

st.markdown("### 📊 Key Variables")
st.markdown("""
- **S**: Current price of the underlying stock  
- **K**: Strike price — the price at which the option allows you to buy/sell  
- **T**: Time to expiration (in years)  
- **r**: Risk-free interest rate (e.g., 10-year Treasury yield)  
- **σ (volatility)**: Standard deviation of stock returns  
- **N(x)**: CDF of the standard normal distribution — interpreted as probabilities under a risk-neutral framework
""")

st.markdown("### 🧮 Black-Scholes Formulas")

st.latex(r"d_1 = \frac{\ln(S/K) + (r + \frac{\sigma^2}{2})T}{\sigma \sqrt{T}}")
st.markdown("**d₁ Interpretation:** Standardized z-score measuring how far above or below the strike the expected stock price is.")

st.latex(r"d_2 = d_1 - \sigma \sqrt{T}")
st.markdown("**d₂ Interpretation:** Risk-neutral probability that the option finishes in-the-money.")

st.latex(r"C = S N(d_1) - K e^{-rT} N(d_2)")
st.markdown("**Call price:** Present value of expected payoff under the risk-neutral measure.")

st.latex(r"P = K e^{-rT} N(-d_2) - S N(-d_1)")
st.markdown("**Put price:** Opposite payoff structure, benefits when stock is below strike.")

st.markdown("### 🔁 Variable Effects on Option Price")
st.table({
    "Variable": ["S (Stock Price)", "K (Strike Price)", "T (Time)", "σ (Volatility)", "r (Risk-Free Rate)"],
    "Call Price": ["↑", "↓", "↑", "↑", "↑"],
    "Put Price": ["↓", "↑", "↑", "↑", "↓"],
})

st.markdown("### ⚙️ Notes")
st.markdown("""
- Assumes constant volatility and interest rates  
- No arbitrage or transaction costs  
- Stock prices follow a log-normal distribution  
- The model outputs theoretical fair value, not necessarily market price  
- Greeks (Δ, Γ, Θ, Vega, Rho) measure sensitivities and are derived from these formulas
""")

if st.button("Go to Black-Scholes Pricer"):
    st.switch_page("pages/1_Black_Scholes_Pricer.py")

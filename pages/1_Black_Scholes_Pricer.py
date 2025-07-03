import streamlit as st
from black_scholes import BlackScholes
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Black-Scholes Pricer")

# Initialise state so that call and put are only reset when calculate button is pressed
for k, v in {"call_px": None, "put_px": None,
             "call_cost": 100.0, "put_cost": 100.0}.items():
    st.session_state.setdefault(k, v)

# Inputs
S = st.number_input("Underlying Stock Price (S)", value=100.0)
K = st.number_input("Strike Price (K)", value=100.0)
T = st.number_input("Time to Expiration (T in years)", value=1.0)
r = st.number_input("Risk-Free Rate (r) (Currently set at .0429)", value=0.0429)
sigma = st.number_input("Volatility (σ)", value=0.2)

# Option Price Calculation
if st.button("Calculate Option Price"):
    st.session_state.call_px = BlackScholes.call_price(S, K, T, r, sigma)
    st.session_state.put_px = BlackScholes.put_price(S, K, T, r, sigma)

    st.session_state.call_cost = st.session_state.call_px
    st.session_state.put_cost = st.session_state.put_px

    st.success(f"Call Option Price per Share: ${st.session_state.call_px:.2f}")
    st.success(f"Put Option Price per Share: ${st.session_state.put_px:.2f}")

# Sensitivity Heatmaps
st.markdown("---")
st.markdown("### Explore Sensitivity via Heatmap")

min_S = st.slider("Min Stock Price (S)", min_value=float(S * .25), max_value=float(S), value=float(S * 0.8))
max_S = st.slider("Max Stock Price (S)", min_value=float(S), max_value=float(S * 1.5), value=float(S * 1.2))

low  = max(0.05, 0.3 * sigma)
high = min(5.00, 3.0 * sigma)
if high - low < 0.20:
    pad = (0.20 - (high - low)) / 2
    low  = max(0.01, low - pad)
    high = min(5.00, high + pad)

min_vol, max_vol = st.slider(
    "Volatility range (σ)",
    min_value=round(low, 3),
    max_value=round(high, 3),
    value=(round(low,3), round(high,3)),
    step=0.01,
)

resolution = 10
S_range = np.linspace(min_S, max_S, resolution)
vol_range = np.linspace(min_vol, max_vol, resolution)
S_grid, vol_grid = np.meshgrid(S_range, vol_range)

call_prices = np.zeros_like(S_grid)
put_prices = np.zeros_like(S_grid)

for i in range(S_grid.shape[0]):
    for j in range(S_grid.shape[1]):
        call_prices[i, j] = BlackScholes.call_price(S_grid[i, j], K, T, r, vol_grid[i, j])
        put_prices[i, j] = BlackScholes.put_price(S_grid[i, j], K, T, r, vol_grid[i, j])

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots()
    heatmap = ax.imshow(call_prices, cmap="RdYlGn", aspect='auto',
                        extent=[min_S, max_S, min_vol, max_vol], origin='lower')
    ax.set_title("Call Option Price Heatmap")
    ax.set_xlabel("Stock Price (S)")
    ax.set_ylabel("Volatility (σ)")
    fig.colorbar(heatmap, ax=ax, label="Call Price per Share ($)")
    st.pyplot(fig)

with col2:
    fig2, ax2 = plt.subplots()
    heatmap2 = ax2.imshow(put_prices, cmap="RdYlGn", aspect='auto',
                         extent=[min_S, max_S, min_vol, max_vol], origin='lower')
    ax2.set_title("Put Option Price Heatmap")
    ax2.set_xlabel("Stock Price (S)")
    ax2.set_ylabel("Volatility (σ)")
    fig2.colorbar(heatmap2, ax=ax2, label="Put Price per Share($)")
    st.pyplot(fig2)

st.markdown("---")
st.markdown("### PnL Simulation at Expiration")


call_cost = st.number_input(
    "Purchase price of Call (per share)",
    value=st.session_state.call_cost,
    key="call_cost"
)
pnl_S = np.linspace(min_S, max_S, 100)
call_pnl = np.maximum(pnl_S - K, 0) - call_cost

# Call PnL Plot
fig3, ax3 = plt.subplots()
breakeven_call = K + call_cost
ax3.plot(pnl_S, call_pnl, label='Call PnL', color='green')
ax3.axhline(0, color='gray', linestyle='--')
ax3.axvline(K, color='red', linestyle=':', label='Strike Price (K)')
ax3.axvline(breakeven_call, color='blue', linestyle='--', label='Breakeven')
ax3.set_title("Call Option PnL at Expiration PER SHARE")
ax3.set_xlabel("Stock Price at Expiration (S)")
ax3.set_ylabel("Profit / Loss ($)")
ax3.legend()
st.pyplot(fig3)

st.markdown("""
**Call PnL Interpretation:**  
You profit when the stock price rises above the strike price by more than what you paid.  
- Break-even = Strike + Cost
- Max loss = premium paid  
- Upside: unlimited
""")

st.markdown("---")
put_cost = st.number_input(
    "Purchase Price of Put (per share)",
    value=st.session_state.put_cost,
    key="put_cost"
)
put_pnl = np.maximum(K - pnl_S, 0) - put_cost

# Put PnL plot
fig4, ax4 = plt.subplots()
breakeven_put = K - put_cost
ax4.plot(pnl_S, put_pnl, label='Put PnL', color='purple')
ax4.axhline(0, color='gray', linestyle='--')
ax4.axvline(K, color='red', linestyle=':', label='Strike Price (K)')
ax4.axvline(breakeven_put, color='blue', linestyle='--', label='Breakeven')
ax4.set_title("Put Option PnL at Expiration PER SHARE")
ax4.set_xlabel("Stock Price at Expiration (S)")
ax4.set_ylabel("Profit / Loss ($)")
ax4.legend()
st.pyplot(fig4)

st.markdown("""
**Put PnL Interpretation:**  
You profit when the stock falls below the strike price by more than what you paid.  
- Break-even = Strike - Cost
- Max loss = premium paid  
- Max gain = when stock goes to 0  
""")

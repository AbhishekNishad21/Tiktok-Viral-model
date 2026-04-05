import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="TikTok Viral Model", layout="wide")

# ----------------------------
# TITLE
# ----------------------------
st.title("📱 TikTok Viral Spread Simulator")
st.markdown("### 🚀 Growth • Peak • Decay Analysis")

# ----------------------------
# SIDEBAR
# ----------------------------
st.sidebar.header("⚙️ Simulation Controls")

beta = st.sidebar.slider("Sharing Rate (β)", 0.0, 1.0, 0.3)
gamma = st.sidebar.slider("Decay Rate (γ)", 0.0, 1.0, 0.1)
alpha = st.sidebar.slider("Influence Rate (α)", 0.0, 1.0, 0.5)
delta = st.sidebar.slider("Forgetting Rate (δ)", 0.0, 1.0, 0.05)

initial_viewers = st.sidebar.slider("Initial Viewers", 10, 1000, 100)
time_steps = st.sidebar.slider("Time Steps", 10, 100, 50)

# ----------------------------
# SIMULATION
# ----------------------------
V = np.zeros(time_steps)
S = np.zeros(time_steps)
P = np.zeros(time_steps)

V[0] = initial_viewers
S[0] = 10

for t in range(1, time_steps):
    dS = beta * V[t-1] - gamma * S[t-1]
    dV = alpha * S[t-1] - delta * V[t-1]

    S[t] = max(S[t-1] + dS, 0)
    V[t] = max(V[t-1] + dV, 0)
    P[t] = max(initial_viewers - V[t] - S[t], 0)

# ----------------------------
# METRICS (TOP CARDS)
# ----------------------------
peak_views = int(max(V))
final_viewers = int(V[-1])

col1, col2 = st.columns(2)

col1.metric("🔥 Peak Views", peak_views)
col2.metric("📉 Final Views", final_viewers)

# ----------------------------
# GRAPH SECTION
# ----------------------------
st.subheader("📊 Viral Growth Curve")

fig, ax = plt.subplots()

ax.plot(V, label="Viewers", linewidth=3)
ax.plot(S, label="Sharers", linestyle='--')
ax.plot(P, label="Passive Users", linestyle=':')

# Highlight Peak
peak_index = np.argmax(V)
ax.scatter(peak_index, peak_views)
ax.text(peak_index, peak_views, " Peak", fontsize=10)

ax.set_xlabel("Time")
ax.set_ylabel("Users")
ax.legend()

st.pyplot(fig)

# ----------------------------
# NETWORK SECTION
# ----------------------------
st.subheader("🌐 Network Structure")

num_nodes = st.slider("Number of Users", 10, 100, 30)

G = nx.erdos_renyi_graph(num_nodes, 0.1)

fig2, ax2 = plt.subplots()
nx.draw(G, node_size=80, ax=ax2)

st.pyplot(fig2)

# ----------------------------
# INTERVENTION BUTTON
# ----------------------------
st.subheader("🛑 Control Strategy")

if st.button("Apply Algorithm Control"):
    st.warning("Sharing rate reduced! Viral spread slowed.")